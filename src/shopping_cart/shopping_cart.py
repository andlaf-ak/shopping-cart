from shopping_cart.receipt import Receipt



class UnderageCustomerError(Exception):
    pass

class ShoppingCart:
    def __init__(self):
        self.products = {}

    def add_product(self, product, quantity=1):
        self.products[product.name] = (product, quantity)

def checkout(shopping_cart, customer, pricing_model):
    # Check age restrictions
    for product, _ in shopping_cart.products.values():
        if getattr(product, 'age_threshold', None) and customer.age < product.age_threshold:
            raise UnderageCustomerError(f"Customer is underage for product: {product.name}")

    items = []
    total = 0
    for product, quantity in shopping_cart.products.values():
        price_info = pricing_model.calculate_price(product, quantity)

        unit_price = price_info['unit_price']
        original_price = price_info['original_price']
        total_price = price_info['total_price']
        discount = price_info['discount']

        discount_text = f" - {str(discount)} (offer {price_info['offer_name']} applied)" if discount else ""
        
        item_prefix = f"{product.name} at {str(unit_price)} x {price_info['original_quantity']} = " 

        if discount:
            line = f"{item_prefix}{original_price} - {discount} (offer {price_info['offer_name']} applied) = {str(total_price)}"
        else:
            line = f"{item_prefix}{str(total_price)}"

        items.append(line)
        total += total_price.amount 
    return Receipt(items, total)

