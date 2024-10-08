from app.db.models import Product as ProductModel
from app.schemas.product import Product
import pytest
from fastapi.exceptions import HTTPException

from app.use_cases.product import ProductUseCases

def test_add_product_uc(db_session, categories_on_db):
    uc = ProductUseCases(db_session)
    product = Product(
        name="Camisa Polo",
        slug="camisa-polo",
        price=22.87,
        stock=4
    )

    uc.add_product(product=product, category_slug=categories_on_db[0].slug)

    product_on_db = db_session.query(ProductModel).first();

    assert product_on_db is not None
    assert product_on_db.name == product.name
    assert product_on_db.slug == product.slug
    assert product_on_db.price == product.price
    assert product_on_db.stock == product.stock
    assert product_on_db.category.name == categories_on_db[0].name

    db_session.delete(product_on_db)
    db_session.commit()


def test_add_product_uc_invalid_category(db_session):
    uc = ProductUseCases(db_session)
    product = Product(
        name="Camisa Polo",
        slug="camisa-polo",
        price=22.87,
        stock=4
    )

    with pytest.raises(HTTPException):
        uc.add_product(product=product, category_slug='invalid')

def test_update_product(db_session, product_on_db):
    product = Product(
        name="Camisa Regata",
        slug="camisa-regata",
        price=21.87,
        stock=42
    )

    uc = ProductUseCases(db_session=db_session)
    uc.update_product(id=product_on_db.id, product=product)

    product_updated_on_db = db_session.query(ProductModel).filter_by(id=product_on_db.id).first();

    assert product_updated_on_db is not None
    assert product_updated_on_db.name == product.name
    assert product_updated_on_db.slug == product.slug
    assert product_updated_on_db.price == product.price
    assert product_updated_on_db.stock == product.stock

def test_update_product_invalid_id(db_session):
    product = Product(
        name="Camisa Regata",
        slug="camisa-regata",
        price=21.87,
        stock=42
    )

    uc = ProductUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.update_product(id=1, product=product)

def test_proccess_csv_data(df, db_session):
    uc = ProductUseCases(db_session=db_session)
    
    response = uc.proccess_csv_data(df=df, db_session=db_session)

    products = db_session.query(ProductModel).all();

    assert len(products) == 2

def test_proccess_csv_data_invalid(df, db_session):
    uc = ProductUseCases(db_session=db_session)
    uc.proccess_csv_data(df=df, db_session=db_session)

    products = db_session.query(ProductModel).all();

    assert len(products) == 2