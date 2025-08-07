from shopping_cart.monetary_amount import Money
from shopping_cart.product_offer import ProductOffer
from typing import Dict, Optional, Any

class PricingModel:
    def __init__(self, default_policy: Dict[str, Money], product_offers: Optional[Dict[str, ProductOffer]] = None) -> None:
        self.policy: Dict[str, Money] = default_policy
        self.product_offers: Dict[str, ProductOffer] = product_offers or {}

    def calculate_price(self, product: Any, quantity: int) -> Dict[str, Any]:
        if not hasattr(product, "name"):
            raise TypeError("product must have a 'name' attribute")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer")
        unit_price = self.policy[product.name]
        offer = self.product_offers.get(product.name)
        if offer:
            offer_result = offer.apply(unit_price, quantity)
            return {
                "product": product,
                "unit_price": unit_price,
                "original_quantity": quantity,
                **offer_result
            }
        else:
            total_price = Money(unit_price.amount * quantity, unit_price.currency.code)
            return {
                "product": product,
                "unit_price": unit_price,
                "original_quantity": quantity,
                "adjusted_quantity": quantity,
                "total_price": total_price,
                "offer_name": "",
                "original_price": total_price,
                "discount": Money(0, unit_price.currency.code)
            }
