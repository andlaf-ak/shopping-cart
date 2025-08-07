from dataclasses import dataclass, field

@dataclass(frozen=True)
class Currency:
    code: str = field()
    SUPPORTED_CURRENCIES = {"USD", "GBP"}

    def __post_init__(self):
        code_upper = self.code.upper()
        if code_upper not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {code_upper}. Supported currencies are: {', '.join(self.SUPPORTED_CURRENCIES)}.")
        object.__setattr__(self, "code", code_upper)

    def __str__(self):
        symbols = {"GBP": "£", "USD": "$"}
        return f"{symbols.get(self.code, self.code)}"
