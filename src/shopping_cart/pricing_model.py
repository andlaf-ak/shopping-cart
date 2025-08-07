from shopping_cart.monetary_amount import Money


class PricingModel:
    """
    Handles product pricing and offer application for a shopping cart.
    """
    def __init__(self, default_policy, product_offers=None):
        """
        :param default_policy: dict mapping product names to Money objects
        :param product_offers: dict mapping product names to ProductOffer objects
        """
        self.policy = default_policy
        self.product_offers = product_offers or {}

    def calculate_price(self, product, quantity: int):
        """
        Calculate the price for a product and quantity, applying any offers.
        :param product: Product object
        :param quantity: int, number of items
        :return: dict with pricing details
        """
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
                "discount": None
            }
