SYMBOLS = {"GBP": '£', "USD": '$'}

class Currency:
    def __init__(self, code):
        self.code = code
        self.symbol = SYMBOLS.get(code, code)
