class PricingModel:
    def __init__(self, default_policy, product_offers=None):
        self.policy = default_policy
        self.product_offers = product_offers or {}

    def calculate_price(self, product, quantity):

        unit_price = self.policy[product.name].amount
        offer = self.product_offers.get(product.name)
        adjusted_quantity = quantity

        if offer:
            if offer.name == "3x2":
                adjusted_quantity = quantity // 3 * 2 + quantity % 3
            
            elif offer.name == "buy-1-get-1-free":
                adjusted_quantity = (quantity + 1) // 2

        total_price = unit_price * adjusted_quantity

        return {
            "product": product,
            "unit_price": unit_price,
            "original_quantity": quantity,
            "adjusted_quantity": adjusted_quantity,
            "total_price": total_price,
            "offer_name": "" if not offer else offer.name
        }
