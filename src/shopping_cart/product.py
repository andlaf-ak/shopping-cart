class Product:
    def __init__(self, name):
        self.name = name


class PricedProduct:
    def __init__(self, product, price):
        self.product = product
        self.price = price