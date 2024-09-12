from app.db.connections import Session
from app.db.models import Category as CategoryModel
from app.db.models import Product as ProductModel
import pytest
import pandas as pd
import io

@pytest.fixture()
def db_session():
    try:
        session = Session()
        yield session
    finally: 
        session.close()

@pytest.fixture()
def categories_on_db(db_session):
    categories = [
        CategoryModel(name="Roupa", slug="roupa"),
        CategoryModel(name="Carro", slug="carro"),
        CategoryModel(name="Itens de lavanderia", slug="itens-de-lavanderia"),
        CategoryModel(name="Decoracao ", slug="decoracao"),
    ]

    for category in categories:
        db_session.add(category)
    db_session.commit()

    for category in categories:
        db_session.refresh(category)

    yield categories

    for category in categories:
        db_session.delete(category)
    db_session.commit()

@pytest.fixture()
def product_on_db(db_session):
    category = CategoryModel(name="Roupa teste", slug="roupa-teste")
    db_session.add(category)
    db_session.commit()

    product = ProductModel(
        name="Camisa Polo",
        slug="camisa-polo",
        price=22.87,
        stock=4,
        category_id=category.id
    )

    db_session.add(product)
    db_session.commit()

    yield product

    db_session.delete(product)
    db_session.delete(category)
    db_session.commit()

@pytest.fixture()
def product_on_csv_data():
    data = {
        "name": ["Acucar", "Feijao"],
        "slug": ["acucar, feijao"],
        "price": [19.99, 29.9],
        "stock": [100, 150]
    }

    pd.DataFrame(data)
    csv_buffer = io.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    return csv_buffer