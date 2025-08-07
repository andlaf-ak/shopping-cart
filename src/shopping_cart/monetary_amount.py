from shopping_cart.currency import Currency


class Money:
    """
    Represents a monetary value in minor units (e.g., pence, cents) and currency.
    """
    SUPPORTED_CURRENCIES = {"USD", "GBP"}

    def __init__(self, amount: int, currency: str) -> None:
        """
        :param amount: int, value in minor units
        :param currency: str, currency code
        """
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("Amount must be a non-negative integer (in minor units)")
        currency = currency.upper()
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency}. Supported currencies are: {', '.join(self.SUPPORTED_CURRENCIES)}.")
        self.amount: int = amount
        self.currency: Currency = Currency(currency)

    def __str__(self) -> str:
        """Return formatted string with currency symbol and amount."""
        return f"{str(self.currency)}{self.amount / 100:.2f}"
    
    def minus(self, other):
        if self.currency.code != other.currency.code:
            raise ValueError("Cannot subtract amounts with different currencies")
        return Money(self.amount - other.amount, self.currency.code)
