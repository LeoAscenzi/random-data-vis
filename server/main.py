from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaConsumer
import random

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

                # print(orderBook.to_json())
                # print("\n")
                
                #Enqueue the latest update only
                await queue.put({"security": sc,
                                 "topBid": orderBook.get_top(sc, "Bid"), 
                                 "topAsk": orderBook.get_top(sc, "Ask"), 
                                 "spread": orderBook.get_spread(sc)})
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
            active_order_count = orderBook.get_order_count()
            # print(f"Active orders: {active_order_count}")
            to_cancel = orderBook.get_random_order_id()
            # print(f"Want to cancel {to_cancel}")
            if active_order_count > 4 and to_cancel is not None:
                sc = orderBook.get_order_by_id(to_cancel)["sc"]
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
    print("Starting up creating async task")
    consumer_task: asyncio.Task = asyncio.create_task(consume())
    cancel_random: asyncio.Task = asyncio.create_task(cancel())
    yield
    consumer_task.cancel()
    cancel_random.cancel()
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

