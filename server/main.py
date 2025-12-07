from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaConsumer

from dotenv import load_dotenv
import os

load_dotenv()
kafka_url = os.getenv("KAFKA_URL")
retry_interval = 5

topics = ['trade-bids', 'trade-asks']

queue = asyncio.Queue()

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
                data = msg.value.decode()
                print(data)
                await queue.put(data)
        except Exception as e:
            print(f"Disconnected from kafka with: {e}, retrying in {retry_interval} seconds")
            await asyncio.sleep(retry_interval)
        finally:
            await consumer.stop()
            print("Stopped consumer")

        await asyncio.sleep(retry_interval)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up creating async task")
    kafka_task = asyncio.create_task(consume())
    yield
    kafka_task.cancel()
    try:
        await kafka_task
    except asyncio.CancelledError:
        pass
    print("Done")

app = FastAPI(lifespan=lifespan)

origins = [
    "*",
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await queue.get()
        await websocket.send_json(data)

