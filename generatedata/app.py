import random
import time
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from confluent_kafka import Producer


trade_type: list = ['Bid', 'Ask']
sec_labels: list = ["RTX", "MLP"]

def connect_and_send(data_count: int, delay: float):
    p = Producer({'bootstrap.servers': 'broker:29092'})
    i = 0
    while(i < data_count):
        d = {'type': random.choice(trade_type), 
             'price': str(round(random.uniform(1.0, 100.0), 2)), 
             'security': random.choice(sec_labels),
             'order_id': str(uuid.uuid4())
             }
        print(d)
        p.poll(0)
        if(d['type'] =="Bid"):
            p.produce('trade-bids', str(d).encode('utf-8'))
        if(d['type'] =="Ask"):
            p.produce('trade-asks', str(d).encode('utf-8'))
        
        time.sleep(delay)
        i+=1

    p.flush()

app = FastAPI()

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

@app.post("/createdata")
def start_data(data_count: int, delay: float):
    connect_and_send(data_count, delay)
