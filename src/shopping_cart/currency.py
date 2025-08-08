class Currency:
    SUPPORTED_CURRENCIES = {"USD", "GBP"}

    def __init__(self, code: str) -> None:
        code_upper = code.upper()
        if code_upper not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {code_upper}. Supported currencies are: {', '.join(self.SUPPORTED_CURRENCIES)}.")
        self.code = code_upper

    def __str__(self):
        symbols = {"GBP": "£", "USD": "$"}
        return f"{symbols.get(self.code, self.code)}"
