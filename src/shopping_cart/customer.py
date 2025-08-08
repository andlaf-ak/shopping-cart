class Customer:
    def __init__(self, age: int) -> None:
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer")
        self.age = age
