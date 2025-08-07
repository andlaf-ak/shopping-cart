from shopping_cart.monetary_amount import Money

class ProductOffer:
    """
    Represents a special offer for a product (e.g., 3x2, buy-1-get-1-free, 3-for-X).
    """
    def __init__(self, name: str, alternate_price: 'Money' = None) -> None:
        """
        :param name: str, offer type
        :param alternate_price: Money, alternate price for some offers
        """
        self.name = name
        self.alternate_price = alternate_price

    def apply(self, unit_price: 'Money', quantity: int) -> dict:
        """
        Apply the offer to a product and quantity.
        :param unit_price: Money, price per item
        :param quantity: int, number of items
        :return: dict with adjusted quantity, total price, offer name, original price, and discount
        """
        original_price = Money(unit_price.amount * quantity, unit_price.currency.code)
        adjusted_quantity = quantity
        total_price = original_price
        offer_name = self.name
        if self.name == "3x2":
            adjusted_quantity = quantity // 3 * 2 + quantity % 3
            total_price = Money(unit_price.amount * adjusted_quantity, unit_price.currency.code)
        elif self.name == "buy-1-get-1-free":
            adjusted_quantity = (quantity + 1) // 2
            total_price = Money(unit_price.amount * adjusted_quantity, unit_price.currency.code)
        elif self.name == "3-for-X" and self.alternate_price:
            offer_name = f"3-for-{self.alternate_price}"
            num_groups = quantity // 3
            remainder = quantity % 3
            total_price = Money(num_groups * self.alternate_price.amount + remainder * unit_price.amount, unit_price.currency.code)
        discount = original_price.minus(total_price)
        return {
            "adjusted_quantity": adjusted_quantity,
            "total_price": total_price,
            "offer_name": offer_name,
            "original_price": original_price,
            "discount": discount
        }