from shopping_cart.money import Money
from typing import Optional, Dict, Any
class ProductOffer:
    OFFER_3X2 = "3x2"
    OFFER_B1G1F = "buy-1-get-1-free"
    OFFER_3_FOR_X = "3-for-X"

    def __init__(self, name: str, alternate_price: Optional['Money'] = None) -> None:
        self.name = name
        self.alternate_price = alternate_price

    def apply(self, unit_price: 'Money', quantity: int) -> Dict[str, Any]:
        if not isinstance(unit_price, Money):
            raise TypeError("unit_price must be a Money instance")

        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")

        original_price = Money(unit_price.amount * quantity, unit_price.currency.code)
        adjusted_quantity = quantity
        total_price = original_price
        offer_name = self.name

        if self.name == self.OFFER_3X2:
            adjusted_quantity = quantity // 3 * 2 + quantity % 3
            total_price = Money(unit_price.amount * adjusted_quantity, unit_price.currency.code)

        elif self.name == self.OFFER_B1G1F:
            adjusted_quantity = (quantity + 1) // 2
            total_price = Money(unit_price.amount * adjusted_quantity, unit_price.currency.code)

        elif self.name == self.OFFER_3_FOR_X:
            if not self.alternate_price:
                raise ValueError("alternate_price must be provided for 3-for-X offer")
            offer_name = f"3-for-{self.alternate_price}"
            num_groups = quantity // 3
            remainder = quantity % 3
            total_price = Money(num_groups * self.alternate_price.amount + remainder * unit_price.amount, unit_price.currency.code)

        discount = original_price.minus(total_price)

        # Ensure discount is non-negative
        if discount.amount < 0:
            discount = Money(0, discount.currency.code)

        return {
            "adjusted_quantity": adjusted_quantity,
            "total_price": total_price,
            "offer_name": offer_name,
            "original_price": original_price,
            "discount": discount
        }