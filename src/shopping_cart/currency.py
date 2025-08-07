class Currency:
    def __init__(self, code):
        self.code = code

    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.code == other.code
        return False

    def __hash__(self):
        return hash(self.code)

    def __str__(self):
        return self.code

    def __repr__(self):
        return f"Currency({self.code})"