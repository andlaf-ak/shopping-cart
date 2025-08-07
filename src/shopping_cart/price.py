from shopping_cart.currency import Currency


class Price:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = Currency(currency)
