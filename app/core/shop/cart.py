class Cart:
    def __init__(self):
        self.items = []

    def add(self, item, price):
        self.items.append((item, price))

    def remove(self, item):
        for i, (name, _) in enumerate(self.items):
            if name == item:
                self.items.pop(i)
                return
        raise ValueError(f"Item '{item}' not found in cart")

    def total(self):
        return sum(price for _, price in self.items)

    def count(self):
        return len(self.items)
