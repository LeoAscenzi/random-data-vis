import random
from data.bookentry import BookEntry

class OrderBook:
    def __init__(self):
        self.orders: dict[str, BookEntry] = {}
        self.orders_by_id = {}

    def add_security(self, sec: str, req_type: str = None, price: float = None, id: str = None):
        if sec not in self.orders:
            self.orders[sec] = BookEntry()
        else:
            print(f"{sec} already exists within orderbook")
        
        if req_type and price and id is not None:
            self.add_order(sec, req_type, price, id)

    def add_order(self, sec: str, req_type: str, price: float, id: str):
        self.orders[sec].add_order(req_type, price, id)
        if(req_type == "Bid"):
            self.orders_by_id[id] = {"sc": sec, "pr": -price, "tp": req_type}
        else:
            self.orders_by_id[id] = {"sc": sec, "pr": price, "tp": req_type}

    def remove_order(self, sec: str, req_type: str, price: float, id: str):
        if(self.orders_by_id[id]):
            del self.orders_by_id[id]
            self.orders[sec].remove_order(req_type, price, id)
        else:
            print(f"Order ID {id} not in orders")

    def get_spread(self, sec: str):
        return self.orders[sec].get_spread()
    
    def get_top(self, sec: str, req_type: str):
        return self.orders[sec].get_top(req_type)

    def remove_security(self, sec: str):
        self.orders[sec].cleanup()
        del self.orders[sec]
        print(f"{sec} removed from dictionary")

    def contains_security(self, sec: str):
        return sec in self.orders
    
    def get_order_count(self):
        return len(self.orders_by_id)
    
    def cancel_order_by_id(self, id: str):
        if(self.orders_by_id[id]):
            order = self.orders_by_id[id]
            sc = order["sc"]
            tp = order["tp"]
            pr = order["pr"]
            self.remove_order(sc, tp, pr, id)
        else:
            print(f"Order ID {id} not in orders")

    def get_order_by_id(self, id: str):
        if(id in self.orders_by_id):
            return self.orders_by_id[id]
        else:
            print("Not in orders")
            return None

    def get_random_order_id(self):
        if not self.orders_by_id:
            return None
        return random.choice(list(self.orders_by_id.keys()))

    def to_json(self):
        return {sec: self.orders[sec].to_json() for sec in self.orders}
    
    def to_spread_json(self):
        return {sec: self.orders[sec].to_spread_json() for sec in self.orders if self.get_spread(sec) is not None}
    
    def __str__(self):
        return ",\n".join([f"key={key}:entry=[{self.orders[key]}]" for key in self.orders])
    