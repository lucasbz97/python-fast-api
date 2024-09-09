from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.db.models import Product as ProductModel

client = TestClient(app)

def test_add_product_route(db_session, categories_on_db):
    body = {
        "category_slug": categories_on_db[0].slug,
        "product": {
            "name": "Camisa Polo",
            "slug": "camisa-polo",
            "price": 29.87,
            "stock": 4
        }
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 1

    db_session.delete(products_on_db[0])
    db_session.commit()

def test_add_product_invalid_category_slug(db_session, categories_on_db):
    body = {
        "category_slug": 'invalid',
        "product": {
            "name": "Camisa Polo",
            "slug": "camisa-polo",
            "price": 29.87,
            "stock": 4
        }
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    products_on_db = db_session.query(ProductModel).all()

    assert len(products_on_db) == 0