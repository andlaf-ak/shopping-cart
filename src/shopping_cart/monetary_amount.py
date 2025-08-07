from shopping_cart.currency import Currency


class MonetaryAmount:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = Currency(currency)
    
    def __str__(self):
        return f"{str(self.currency)}{self.amount / 100:.2f}"
