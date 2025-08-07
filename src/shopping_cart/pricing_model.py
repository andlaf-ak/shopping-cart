class PricingModel:
    def __init__(self, default_policy, product_offers=None):
        self.policy = default_policy
        self.product_offers = product_offers or {}

    def calculate_price(self, product, quantity):

        unit_price = self.policy[product.name].amount
        offer = self.product_offers.get(product.name)
        offer_name = "" if not offer else offer.name
        adjusted_quantity = quantity

        total_price = unit_price * adjusted_quantity
        if offer:
            if offer_name == "3x2":
                adjusted_quantity = quantity // 3 * 2 + quantity % 3
                total_price = unit_price * adjusted_quantity
                
            elif offer_name == "buy-1-get-1-free":
                adjusted_quantity = (quantity + 1) // 2
                total_price = unit_price * adjusted_quantity
                
            elif offer_name == "3-for-X":
                offer_name = f"3-for-{offer.alternate_price.amount // 100}"
                # For every group of 3, use alternate price, rest use unit price
                num_groups = quantity // 3
                remainder = quantity % 3
                total_price = num_groups * offer.alternate_price.amount + remainder * unit_price

        return {
            "product": product,
            "unit_price": unit_price,
            "original_quantity": quantity,
            "adjusted_quantity": adjusted_quantity,
            "total_price": total_price,
            "offer_name": offer_name
        }
