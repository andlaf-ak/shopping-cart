from typing import Optional


class Product:
    def __init__(self, name: str, age_threshold: Optional[int] = None) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if age_threshold is not None and (
            not isinstance(age_threshold, int) or age_threshold < 0
        ):
            raise ValueError("age_threshold must be a non-negative integer or None")
        self.name = name
        self.age_threshold = age_threshold
