from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaConsumer
import time

from dotenv import load_dotenv
import os
import ast

from data.orderbook import OrderBook
from models.orderrequest import OrderRequest

load_dotenv()
kafka_url: str = os.getenv("KAFKA_URL")
retry_interval: int = 5

topics: list = ['trade-bids', 'trade-asks']

queue: asyncio.Queue = asyncio.Queue()
orderBook: OrderBook = OrderBook()

async def consume():
    while(1):
        try:
            print(f"Trying to connect to kafka at: {kafka_url}")
            consumer = AIOKafkaConsumer(
                                *topics,
                                bootstrap_servers=kafka_url,
                                auto_offset_reset="latest")
            await consumer.start()
            print(f"Consumer started on {kafka_url}")
            async for msg in consumer:
                # Decode byte, then deserialize to dict, then spread to dataclass
                req: OrderRequest = OrderRequest(**ast.literal_eval(msg.value.decode()))
                tp: str = req.type
                sc: str = req.security
                pr: float = float(req.price)
                id: str = req.order_id

                if not orderBook.contains_security(sc):
                    orderBook.add_security(sc, tp, pr, id)
                else:
                    orderBook.add_order(sc, tp, pr, id)

                #Enqueue the latest update only
                await queue.put({"security": sc,
                                 "topBid": orderBook.get_top(sc, "Bid"), 
                                 "topAsk": orderBook.get_top(sc, "Ask"), 
                                 "spread": orderBook.get_spread(sc)})
                
                # If the stats have just been started, set count to and log start time
                if(app.state.count_total == 0):
                    app.state.start_time = time.time()
                app.state.count_total+=1

                # When we consume the target, stop the test
                if(app.state.target_count == app.state.count_total):
                    app.state.end_time = time.time()
        except Exception as e:
            print(f"Disconnected from kafka with: {e}, retrying in {retry_interval} seconds")
            await asyncio.sleep(retry_interval)
        finally:
            await consumer.stop()
            print("Stopped consumer")

        await asyncio.sleep(retry_interval)

async def cancel():
    while True:
        try:
            to_cancel = orderBook.get_random_order_id()
            if to_cancel is not None:
                sc = orderBook.get_order_by_id(to_cancel)["sc"]
                if(orderBook.get_count(sc, "Bid") > 4 and orderBook.get_count(sc, "Ask") > 4):
                    orderBook.cancel_order_by_id(to_cancel)
                    await queue.put({"security": sc,
                                    "topBid": orderBook.get_top(sc, "Bid"), 
                                    "topAsk": orderBook.get_top(sc, "Ask"), 
                                    "spread": orderBook.get_spread(sc)})
        except Exception as e:
            print(f"Error in cancel task: {e}")
        await asyncio.sleep(0.001)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.count_total = 0
    app.state.start_time = None
    app.state.end_time = None
    app.state.target_count = 0

    print("Starting up creating async task")
    consumer_task: asyncio.Task = asyncio.create_task(consume())
    cancel_random: asyncio.Task = asyncio.create_task(cancel())
    yield
    consumer_task.cancel()
    cancel_random.cancel()
    del app.state.count_total
    del app.state.count_tostart_timetal
    del app.state.end_time
    del app.state.target_count

    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
    print("Done")

app = FastAPI(lifespan = lifespan)

origins = [
    "http://localhost:5173",
    "https://random-data-vis.vercel.app",
    "https://www.random-data-vis.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def healthcheck():
   return {"status": "App is up!"}

@app.get("/get-all-data")
def get_all_data():
    return orderBook.to_json()

@app.get("/get-all-spread")
def get_all_spread():
    return orderBook.to_spread_json()

@app.get("/reset-all-data")
def reset_all_data():
    orderBook.cleanup()
    return {"status" : "Cleaned up!"}

@app.get("/poll-stats")
def poll_stats():
    current_time = time.time()
    status = "not_started"
    elapsed = 0
    
    if(app.state.start_time is not None):
        status = "running"
        if(app.state.end_time is not None):
            current_time = app.state.end_time
            status = "done"
        elapsed = current_time - app.state.start_time
    
    return {"status": status,
            "current_count": app.state.count_total, 
            "elapsed": elapsed}

@app.post("/prepare-stats")
def prepare_stats(data_count: int):
    if(app.state.end_time is not None):
        return {"status" : "not_ready"}
    app.state.count_total = 0
    app.state.end_time = None
    app.state.target_count = data_count
    return {"status" : "ready"}
        

connections: set = set()
dead_sockets: set = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)
    try:
        while True:
            data = await queue.get()
            for socket in connections:
                try:
                    await socket.send_json(data)
                except Exception:
                    dead_sockets.add(socket)
            for socket in dead_sockets:
                connections.remove(socket)
            dead_sockets.clear()
    except Exception as e:
        print(f"Some error occured: {e}")
    finally:
        connections.remove(websocket)

