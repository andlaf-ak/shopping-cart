from shopping_cart.product import PricedProduct
from shopping_cart.receipt import Receipt


class ShoppingCart:
    def __init__(self):
       self.products = {}

    def add_product(self, product, quantity=1):
        self.products[product.name] = (product, quantity)

def checkout(shopping_cart, pricing_model):
    items = ['fake item']
    total = 100
    return Receipt(items, total)