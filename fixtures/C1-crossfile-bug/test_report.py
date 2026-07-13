from store import Store
from orders import OrderBook
from report import fulfillment_report


def test_exact_stock_can_be_sold():
    s = Store()
    s.add("apple", 5)
    book = OrderBook(s)
    assert book.place(1, "apple", 3)
    assert book.place(2, "apple", 2)
    r = fulfillment_report(book)
    assert r["confirmed"] == 2
    assert r["units_sold"] == 5
    assert s.available("apple") == 0


def test_oversell_is_rejected():
    s = Store()
    s.add("pen", 2)
    book = OrderBook(s)
    assert not book.place(1, "pen", 3)
    r = fulfillment_report(book)
    assert r["rejected"] == 1
    assert s.available("pen") == 2


def test_mixed_orders():
    s = Store()
    s.add("book", 10)
    book = OrderBook(s)
    assert book.place(1, "book", 4)
    assert book.place(2, "book", 6)
    assert not book.place(3, "book", 1)
    r = fulfillment_report(book)
    assert r == {"confirmed": 2, "rejected": 1, "units_sold": 10}
