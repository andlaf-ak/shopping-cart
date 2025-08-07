from shopping_cart.receipt import Receipt


class ShoppingCart:
    def __init__(self):
       self.products = {}

    def add_product(self, product, quantity=1):
        self.products[product.name] = (product, quantity)

def checkout(shopping_cart, pricing_model):
    items = []
    total = 0
    for product, quantity in shopping_cart.products.values():
        if product.name in pricing_model.policy:
            price = pricing_model.policy[product.name].amount
            cost = price * quantity
            items.append(f"{product.name} at {price} x{quantity} = {cost}")
            total += cost
    return Receipt(items, total)

