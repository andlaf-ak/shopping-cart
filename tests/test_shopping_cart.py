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
