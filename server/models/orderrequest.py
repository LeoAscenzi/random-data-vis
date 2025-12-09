from dataclasses import dataclass

@dataclass
class OrderRequest():
    type: str
    price: float
    security: str
    order_id: str

    def is_bid(self):
        return self.type.lower == "bid"
    def is_ask(self):
        return self.type.lower == "ask"
    
    def __str__(self):
        return f"Req Type: {self.type}, Security: {self.security}, Price: {self.price}, OID: {self.order_id}"