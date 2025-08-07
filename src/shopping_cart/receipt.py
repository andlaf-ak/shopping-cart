from dataclasses import dataclass, field
from typing import Any, List

@dataclass(frozen=True)
class Receipt:
    items: List[Any] = field()
    total: Any = field()
