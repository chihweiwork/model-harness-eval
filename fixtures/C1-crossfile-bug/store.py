class Store:
    """In-memory stock keeping."""

    def __init__(self):
        self._stock = {}

    def add(self, sku, qty):
        self._stock[sku] = self._stock.get(sku, 0) + qty

    def available(self, sku):
        return self._stock.get(sku, 0)

    def reserve(self, sku, qty):
        """Reserve qty units of sku. Returns True on success."""
        if self._stock.get(sku, 0) > qty:
            self._stock[sku] -= qty
            return True
        return False
