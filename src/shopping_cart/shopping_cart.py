from shopping_cart.receipt import Receipt



class UnderageCustomerError(Exception):
    pass

class ShoppingCart:
    def __init__(self):
        self.products = {}

    def add_product(self, product, quantity=1):
        self.products[product.name] = (product, quantity)

    def checkout(self, customer, pricing_model):
        # Check age restrictions
        for product, _ in self.products.values():
            if getattr(product, 'age_threshold', None) and customer.age < product.age_threshold:
                raise UnderageCustomerError(f"Customer is underage for product: {product.name}")

        items = []
        total = 0
        for product, quantity in self.products.values():
            price_info = pricing_model.calculate_price(product, quantity)

            unit_price = price_info['unit_price']
            total_price = price_info['total_price']

            line = f"{product.name} at {str(unit_price)} x{price_info['original_quantity']} = {str(total_price)}"
            if price_info['offer_name']:
                line += f" (offer {price_info['offer_name']} applied)"

            items.append(line)
            total += total_price.amount 
        return Receipt(items, total)

