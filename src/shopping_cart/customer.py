from dataclasses import dataclass, field

@dataclass(frozen=True)
class Customer:
    age: int = field()

    def __post_init__(self):
        if not isinstance(self.age, int) or self.age < 0:
            raise ValueError("Age must be a non-negative integer")