class Currency:
    SUPPORTED_CURRENCIES = {"USD", "GBP"}

    def __init__(self, code):
        code = code.upper()
        if code not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {code}. Supported currencies are: {', '.join(self.SUPPORTED_CURRENCIES)}.")
        self.code = code

    def __str__(self):
        symbols = {"GBP": "£", "USD": "$"}
        return f"{symbols.get(self.code, self.code)}"
