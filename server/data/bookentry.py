from sortedcontainers import SortedDict

class BookEntry:

    def __init__(self):
        self.bids: SortedDict = SortedDict()
        self.asks: SortedDict = SortedDict()

    def add_order(self, req_type: str, price: float, id: str):
        if req_type == "Bid":
            price=-price
        order_type = self.bids if req_type == "Bid" else self.asks
        order_type[price] = id

    def remove_order(self, req_type: str, price: float, id: str):
        order_type = self.bids if req_type == "Bid" else self.asks
        # order_type[price].remove(id)
        # if not order_type[price]:
        del order_type[price]

    def get_spread(self):
        if self.has_bids() and self.has_asks():
            return str(round(self.get_top("Ask") - self.get_top("Bid"), 2))
        else:
            return None
    def get_top(self, req_type: str) -> float:
        order_type = self.bids if req_type == "Bid" else self.asks
        if len(order_type) > 0 and order_type.peekitem(0):
            return (-float(order_type.peekitem(0)[0])) if req_type == "Bid" else float(order_type.peekitem(0)[0])
        else:
            return None
        
    def get_count(self, req_type: str) -> int:
        order_type = self.bids if req_type == "Bid" else self.asks
        return len(order_type)
    
    def has_bids(self):
        return len(self.bids) > 0

    def has_asks(self):
        return len(self.asks) > 0

    def to_spread_json(self):
        if self.has_asks() and self.has_bids():
            d = {}
            return {"topBid": str(self.get_top("Bid")),
                    "topAsk": str(self.get_top("Ask")),
                    "spread": str(self.get_spread())}
    
    def to_json(self):
        return {"bids": dict(self.bids), "asks": dict(self.asks)}

    def __str__(self):
        return f"[bids->{self.bids}, asks->{self.asks}]"