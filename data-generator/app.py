import random
import time
from fastapi import FastAPI
from confluent_kafka import Producer


trade_type = ['Bid', 'Ask']
def connect_and_send(data_count: int, delay: float):
    p = Producer({'bootstrap.servers': 'broker:29092'})
    i = 0
    while(i < data_count):
        d = {'type': random.choice(trade_type), 'price': random.uniform(1.0, 100.0), 'volume': random.randint(1, 1000)}
        print(d)
        p.poll(0)
        p.produce('trade-data', str(d).encode('utf-8'))
        time.sleep(delay)
        i+=1

    p.flush()

app = FastAPI()

@app.get("/")
def healthcheck():
   return {"status": "App is up!"}

@app.post("/start-data")
def start_data(data_count: int, delay: float):
    connect_and_send(data_count, delay)