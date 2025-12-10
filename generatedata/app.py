import random
import time
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from confluent_kafka import Producer


trade_type: list[str] = ['Bid', 'Ask']
sec_config = {"RTX":{"mp":171, "sp":10},
              "MLP":{"mp":50, "sp":15},
              "NVDA":{"mp":185, "sp":2},
              "TSLA":{"mp":439, "sp":8},
              "PLTR":{"mp":181, "sp":5}}

def connect_and_send(data_count: int, delay: float):
    p = Producer({'bootstrap.servers': 'broker:29092'})
    i = 0
    startTime: float = time.time()
    sec_keys: list[str] = list(sec_config.keys())
    while(i < data_count):
        type = random.choice(trade_type)
        sec = random.choice(sec_keys)
        price_mid = sec_config[sec]["mp"]
        price_spread = sec_config[sec]["sp"]

        price = round((price_mid - random.uniform(1,price_spread)),2) if type == "Bid" else round((price_mid+random.uniform(1,price_spread)),2)
        d = {'type': type, 
             'price': str(price), 
             'security': sec,
             'order_id': str(uuid.uuid4())
             }
        print(d)
        p.poll(0)
        if(d['type'] =="Bid"):
            p.produce('trade-bids', str(d).encode('utf-8'))
        if(d['type'] =="Ask"):
            p.produce('trade-asks', str(d).encode('utf-8'))
        
        if(delay != -1):
            time.sleep(delay)
        i+=1
    endTime: float = time.time()

    duration_ms: float = endTime - startTime
    p.flush()
    return (duration_ms, i)


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
    duration_ms, i = connect_and_send(data_count, delay)
    return {"duration": duration_ms, "count": i}
