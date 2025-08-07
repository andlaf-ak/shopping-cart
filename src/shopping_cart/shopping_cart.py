from shopping_cart.receipt import Receipt



class UnderageCustomerError(Exception):
    pass

from typing import Dict, Any

class ShoppingCart:
    def __init__(self) -> None:
        self.products: Dict[str, Any] = {}

    def add_product(self, product: Any, quantity: int = 1) -> None:
        if not hasattr(product, "name"):
            raise TypeError("product must have a 'name' attribute")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("quantity must be a non-negative integer")
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
        total_price = price_info['total_price']
        original_price = price_info.get('original_price', total_price)
        discount = price_info.get('discount', None)
        offer_name = price_info.get('offer_name', "")

        
        item_prefix = f"{product.name} at {str(unit_price)} x {price_info['original_quantity']} = " 

        if offer_name:
            line = f"{item_prefix}{str(original_price)}"
            if discount and discount.amount > 0:
                line += f" - {str(discount)} (offer {offer_name} applied) = {str(total_price)}"
            else:
                line += f" (offer {offer_name} applied) = {str(total_price)}"
        else:
            line = f"{item_prefix}{str(total_price)}"

        items.append(line)
        total += total_price.amount 
    return Receipt(items, total)

