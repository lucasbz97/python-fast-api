from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.db.models import Product as ProductModel
import pandas as pd
import io

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

def test_udpate_product_route(db_session, product_on_db):
    body = {
        "name": "Camisa Polo Update",
        "slug": "camisa-polo-update",
        "price": 23.87,
        "stock": 4
    }
    print(f'produto com id - {product_on_db.id}')
    response = client.put(f'/product/update/{product_on_db.id}', json=body)
    print(f'Resposta recebida: {response.status_code}')

    assert response.status_code == status.HTTP_200_OK
    
    db_session.refresh(product_on_db)

    product_on_db.name == 'Camisa Polo Update'
    product_on_db.slug == 'camisa-polo-update'
    product_on_db.price == 23.87
    product_on_db.stock == 4

def test_udpate_product_invalid_id_route(db_session):
    body = {
        "name": "Camisa Polo Update",
        "slug": "camisa-polo-update",
        "price": 23.87,
        "stock": 4
    }

    response = client.put(f'/product/update/11111', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_upload_csv_route(db_session, product_on_csv_data):
    response = client.post(f'/product/upload-csv', files={"file": ("test.csv", product_on_csv_data, "text/csv")})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status_code":status.HTTP_200_OK }

    products = db_session.query(ProductModel).all()

    assert len(products) == 2

def test_upload_csv_route_invalid_csv_type(db_session, product_on_csv_data):
    response = client.post(f'/product/upload-csv', files={"file": ("test.txt", product_on_csv_data, "text/csv")})

    assert response.status_code == status.HTTP_400_BAD_REQUEST