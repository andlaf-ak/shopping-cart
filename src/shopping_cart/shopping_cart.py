from shopping_cart.receipt import Receipt


class ShoppingCart:
    def __init__(self):
        self.products = {}

    def add_product(self, product, quantity=1):
        self.products[product.name] = (product, quantity)


def checkout(shopping_cart, pricing_model):
    items = []
    total = 0
    for product, quantity in shopping_cart.products.values():
        if product.name in pricing_model.policy:
            price = pricing_model.policy[product.name].amount
            offer_applied = pricing_model.product_offers and product.name in pricing_model.product_offers
            offer_name = ""
            if offer_applied and pricing_model.product_offers[product.name] == "3x2": 
                offer_name = "3x2"
                if pricing_model.product_offers.get(product.name) == "3x2":
                    quantity = quantity // 3 * 2 + quantity % 3
            cost = price * quantity
            items.append(f"{product.name} at {price} x{quantity} = {cost}" + f" (offer {offer_name} applied)" if offer_applied else "")
            total += cost
    return Receipt(items, total)

def can_checkout(customer, shopping_cart):
    for product, _ in shopping_cart.products.values():
        if product.age_threshold and customer.age < product.age_threshold:
            return False
    return True