from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class Product:
    name: str = field()
    age_threshold: Optional[int] = field(default=None)

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        if self.age_threshold is not None and (not isinstance(self.age_threshold, int) or self.age_threshold < 0):
            raise ValueError("age_threshold must be a non-negative integer or None")