class PricingModel:
    def __init__(self, default_policy, product_offers=None):
        self.policy = default_policy
        self.product_offers = product_offers
