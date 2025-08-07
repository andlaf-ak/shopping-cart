from typing import Optional

class Product:
    def __init__(self, name: str, age_threshold: Optional[int] = None) -> None:
        self.name: str = name
        self.age_threshold: Optional[int] = age_threshold