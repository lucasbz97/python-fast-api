from app.schemas.product import Product, ProductInput
import pytest

def test_product_schema():
    product = Product(
        name="Camisa Polo",
        slug="camisa-polo",
        price=22.87,
        stock=4
    )

    assert product.dict() == {
        'name': 'Camisa Polo',
        'slug': 'camisa-polo',
        'price': 22.87,
        'stock': 4
    }

def test_product_schema_invalid_slug():
    with pytest.raises(ValueError):
        product = Product(
            name="Camisa Polo",
            slug="camisa polo",
            price=22.87,
            stock=4
        )

    with pytest.raises(ValueError):
        product = Product(
            name="Camisa Polo",
            slug="Camisa-polo",
            price=22.87,
            stock=4
        )

    with pytest.raises(ValueError):
        product = Product(
            name="Camisa Polo",
            slug="cãmisa-polo",
            price=22.87,
            stock=4
        )

def test_product_schema_invalid_price():
    with pytest.raises(ValueError):
        product = Product(
            name="Camisa Polo",
            slug="camisa-polo",
            price=0,
            stock=4
        )

def test_product_input_schema():
    product = Product (
        name="Camisa Polo",
        slug="camisa-polo",
        price=29.87,
        stock=4
    )

    product_input = ProductInput(
        category_slug='camisa',
        product=product
    )

    assert product_input.dict() == {
        "category_slug": "camisa",
        "product": {
            "name": "Camisa Polo",
            "slug": "camisa-polo",
            "price": 29.87,
            "stock": 4
        }
    }