from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaConsumer

from dotenv import load_dotenv
import os

load_dotenv()

queue = asyncio.Queue()
async def consume():
    consumer = AIOKafkaConsumer('trade-data',
                                bootstrap_servers=os.getenv("KAFKA_URL") + ":" + os.getenv("KAFKA_PORT"),
                                group_id="mygroup", 
                                auto_offset_reset="latest")
    try:
        await consumer.start()
    except Exception:
        print("FAILURE CONNECTING TO FAKFA")
    print("Started consumer?")
    try:
        async for msg in consumer:
            data = msg.value.decode("UTF-8")
            print(data)
            await queue.put(data)
    finally:
        await consumer.stop()
        print("Stopped consumer")

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    "http://localhost:5173",
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

