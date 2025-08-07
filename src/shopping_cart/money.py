from shopping_cart.currency import Currency


from shopping_cart.currency import Currency
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Money:
    amount: int
    currency: Currency
    SUPPORTED_CURRENCIES = {"USD", "GBP"}

    def __init__(self, amount: int, currency: str) -> None:
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("Amount must be a non-negative integer (in minor units)")
        if not isinstance(currency, str):
            raise TypeError("currency must be a string")
        currency_upper = currency.upper()
        if currency_upper not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency_upper}. Supported currencies are: {', '.join(self.SUPPORTED_CURRENCIES)}.")
        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "currency", Currency(currency_upper))

    def __str__(self) -> str:
        return f"{str(self.currency)}{self.amount / 100:.2f}"

    def minus(self, other: Any) -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("Can only subtract Money from Money.")
        if self.currency.code != other.currency.code:
            raise ValueError("Cannot subtract amounts with different currencies")
        return Money(self.amount - other.amount, self.currency.code)
