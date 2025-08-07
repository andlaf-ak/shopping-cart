import pytest


from shopping_cart.customer import Customer
from shopping_cart.price import Price
from shopping_cart.product import Product
from shopping_cart.product_offer import ProductOffer
from shopping_cart.shopping_cart import ShoppingCart, can_checkout, checkout
from shopping_cart.pricing_model import PricingModel


def test_plain_checkout():
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(100, "GBP"),
    })
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 1)
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 1
    assert receipt.total == 1 * pricing_model.policy["pack-of-6-eggs"].amount


def test_complex_checkout():
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(50, "GBP"),
        "bottle-of-milk": Price(111, "GBP"),
        "pack-of-sugar": Price(125, "GBP"),
    })
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 1)
    shopping_cart.add_product(Product("bottle-of-milk"), 6)
    shopping_cart.add_product(Product("pack-of-sugar"), 3)
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 3
    assert receipt.total == 1 * pricing_model.policy["pack-of-6-eggs"].amount + 6 * \
        pricing_model.policy["bottle-of-milk"].amount + \
        3 * pricing_model.policy["pack-of-sugar"].amount

def test_underage_customer_cannot_buy_certain_products():
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 1)
    shopping_cart.add_product(Product("bottle-of-milk"), 6)
    shopping_cart.add_product(Product("pack-of-sugar"), 3)
    shopping_cart.add_product(Product("bottle-of-whisky", 18), 1)
    assert can_checkout(Customer(age=17), shopping_cart) is False

def test_basic_three_for_two_offer():
    product_offers = {
       "pack-of-6-eggs": ProductOffer("3x2"),
    }
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(50, "GBP"),
    }, product_offers)
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 3)
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 1
    assert receipt.total == 2 * pricing_model.policy["pack-of-6-eggs"].amount

def test_complex_three_for_two_offer():
    product_offers = {
       "pack-of-6-eggs": ProductOffer("3x2"),
    }
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(50, "GBP"),
    }, product_offers)
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 8)
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 1
    assert receipt.total == 6 * pricing_model.policy["pack-of-6-eggs"].amount

def test_basic_buy_one_get_one_free_offer():
    product_offers = {
       "pack-of-6-eggs": ProductOffer("buy-1-get-1-free"),
    }
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(50, "GBP"),
    }, product_offers)
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 2)
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 1
    assert receipt.total == 1 * pricing_model.policy["pack-of-6-eggs"].amount

def test_complex_buy_one_get_one_free_offer():
    product_offers = {
       "pack-of-6-eggs": ProductOffer("buy-1-get-1-free"),
    }
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(50, "GBP"),
    }, product_offers)
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 5)
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 1
    assert receipt.total == 3 * pricing_model.policy["pack-of-6-eggs"].amount

def test_basic_3_for_X_policy():
    product_offers = {
       "pack-of-6-eggs": ProductOffer("3-for-X", Price(250, "GBP")),
    }
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(100, "GBP"),
    }, product_offers)
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 3)
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 1
    assert receipt.total == 250 

def test_complex_3_for_X_offer():
    product_offers = {
       "pack-of-6-eggs": ProductOffer("3-for-X", Price(250, "GBP")),
    }
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(100, "GBP"),
    }, product_offers)
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 8)
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 1
    assert receipt.total == 250 * 2 + 100 * 2  # 2 groups of 3 at alternate price, plus 2 at unit price

def test_complex_shopping_cart_with_many_products_and_offers():
    product_offers = {
       "pack-of-6-eggs": ProductOffer("3x2"),
       "bottle-of-milk": ProductOffer("buy-1-get-1-free"),
       "pack-of-sugar": ProductOffer("3-for-X", Price(750, "GBP")),
    }
    pricing_model = PricingModel({
        "pack-of-6-eggs": Price(100, "GBP"),
        "bottle-of-milk": Price(200, "GBP"),
        "pack-of-sugar": Price(300, "GBP"),
        "bottle-of-whisky": Price(500, "GBP"),
    }, product_offers)
    
    shopping_cart = ShoppingCart()
    shopping_cart.add_product(Product("pack-of-6-eggs"), 8)
    shopping_cart.add_product(Product("bottle-of-milk"), 5)
    shopping_cart.add_product(Product("pack-of-sugar"), 10)
    shopping_cart.add_product(Product("bottle-of-whisky"), 1)
    
    receipt = checkout(shopping_cart, pricing_model)
    assert len(receipt.items) == 4
    assert receipt.total == (
        6 * pricing_model.policy["pack-of-6-eggs"].amount + 
        3 * pricing_model.policy["bottle-of-milk"].amount +
        750*3+pricing_model.policy["pack-of-sugar"].amount +
        pricing_model.policy["bottle-of-whisky"].amount
    )
    assert receipt.items[0] == "pack-of-6-eggs at £1.00 x8 = £6.00 (offer 3x2 applied)"
    assert receipt.items[1] == "bottle-of-milk at £2.00 x5 = £6.00 (offer buy-1-get-1-free applied)"
    assert receipt.items[2] == "pack-of-sugar at £3.00 x10 = £25.50 (offer 3-for-£7.50 applied)"
    assert receipt.items[3] == "bottle-of-whisky at £5.00 x1 = £5.00"