class Currency:
    def __init__(self, code):
        self.code = code

    def __str__(self):
        symbols = {"GBP": "£", "USD": "$"}
        return f"{symbols.get(self.code, self.code)}"
