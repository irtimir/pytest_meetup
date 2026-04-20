from core.shop.cart import Cart


class CartStorage:
    def __init__(self, client):
        self.client = client

    def save(self, cart_id, cart):
        data = {item: price for item, price in cart.items}
        self.client.hset(f"cart:{cart_id}", mapping=data)

    def load(self, cart_id):
        cart = Cart()
        data = self.client.hgetall(f"cart:{cart_id}")
        for item, price in data.items():
            cart.add(item, float(price))
        return cart
