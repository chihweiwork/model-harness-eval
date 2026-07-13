from orders import OrderBook


def fulfillment_report(book: OrderBook):
    """Summarize an order book."""
    confirmed = [o for o in book.orders if o["status"] == "confirmed"]
    rejected = [o for o in book.orders if o["status"] == "rejected"]
    return {
        "confirmed": len(confirmed),
        "rejected": len(rejected),
        "units_sold": sum(o["qty"] for o in confirmed),
    }
