from typing import Any, List

class Receipt:
    def __init__(self, items: List[Any], total: Any) -> None:
        self.items = items
        self.total = total
