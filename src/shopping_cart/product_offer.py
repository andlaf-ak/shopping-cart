from shopping_cart.monetary_amount import Money

class ProductOffer:
    def __init__(self, name: str, alternate_price: 'Money' = None) -> None:
        self.name = name
        self.alternate_price = alternate_price

    def apply(self, unit_price: 'Money', quantity: int) -> dict:
        """Return adjusted quantity, total price, and discount for this offer."""
        original_price = Money(unit_price.amount * quantity, unit_price.currency)
        adjusted_quantity = quantity
        total_price = original_price
        offer_name = self.name
        if self.name == "3x2":
            adjusted_quantity = quantity // 3 * 2 + quantity % 3
            total_price = Money(unit_price.amount * adjusted_quantity, unit_price.currency)
        elif self.name == "buy-1-get-1-free":
            adjusted_quantity = (quantity + 1) // 2
            total_price = Money(unit_price.amount * adjusted_quantity, unit_price.currency)
        elif self.name == "3-for-X" and self.alternate_price:
            offer_name = f"3-for-{self.alternate_price}"
            num_groups = quantity // 3
            remainder = quantity % 3
            total_price = Money(num_groups * self.alternate_price.amount + remainder * unit_price.amount, unit_price.currency)
        discount = original_price.minus(total_price)
        return {
            "adjusted_quantity": adjusted_quantity,
            "total_price": total_price,
            "offer_name": offer_name,
            "original_price": original_price,
            "discount": discount
        }