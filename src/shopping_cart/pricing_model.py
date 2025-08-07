from shopping_cart.monetary_amount import Money


class PricingModel:
    def __init__(self, default_policy, product_offers=None):
        self.policy = default_policy
        self.product_offers = product_offers or {}

    def calculate_price(self, product, quantity):
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
            total_price = Money(unit_price.amount * quantity, unit_price.currency)
            return {
                "product": product,
                "unit_price": unit_price,
                "original_quantity": quantity,
                "adjusted_quantity": quantity,
                "total_price": total_price,
                "offer_name": "",
                "original_price": total_price,
                "discount": None
            }
