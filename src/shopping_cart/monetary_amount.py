from shopping_cart.currency import Currency


class Money:
    def __init__(self, amount: int, currency: str) -> None:
        self.amount: int = amount
        self.currency: Currency = Currency(currency)

    def __str__(self) -> str:
        return f"{str(self.currency)}{self.amount / 100:.2f}"
    
    def minus(self, other):
        if self.currency.code != other.currency.code:
            raise ValueError("Cannot subtract amounts with different currencies")
        return Money(self.amount - other.amount, self.currency.code)
