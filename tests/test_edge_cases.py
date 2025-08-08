import pytest
from shopping_cart.money import Money
from shopping_cart.product import Product
from shopping_cart.pricing_model import PricingModel


def test_zero_quantity():
    pricing_model = PricingModel({"item": Money(100, "GBP")})
    product = Product("item")
    result = pricing_model.calculate_price(product, 0)
    assert result["total_price"].amount == 0


def test_negative_quantity():
    pricing_model = PricingModel({"item": Money(100, "GBP")})
    product = Product("item")
    with pytest.raises(ValueError):
        pricing_model.calculate_price(product, -1)


def test_unsupported_currency():
    with pytest.raises(Exception):
        Money(100, "XXX")
