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
        price_info = pricing_model.calculate_price(product, quantity)

        unit_price = price_info['unit_price']
        total_price = price_info['total_price']

        line = f"{product.name} at {str(unit_price)} x{price_info['original_quantity']} = {str(total_price)}"
        if price_info['offer_name']:
            line += f" (offer {price_info['offer_name']} applied)"

        items.append(line)
        total += total_price.amount 
    return Receipt(items, total)


def can_checkout(customer, shopping_cart):
    for product, _ in shopping_cart.products.values():
        if product.age_threshold and customer.age < product.age_threshold:
            return False
    return True