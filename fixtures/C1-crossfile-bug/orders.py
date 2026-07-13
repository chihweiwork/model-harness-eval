from store import Store


class OrderBook:
    """Places orders against a Store."""

    def __init__(self, store: Store):
        self.store = store
        self.orders = []

    def place(self, order_id, sku, qty):
        if self.store.reserve(sku, qty):
            self.orders.append(
                {"id": order_id, "sku": sku, "qty": qty, "status": "confirmed"}
            )
            return True
        self.orders.append(
            {"id": order_id, "sku": sku, "qty": qty, "status": "rejected"}
        )
        return False
