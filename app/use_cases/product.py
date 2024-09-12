from datetime import datetime
from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from app.schemas.product import Product
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status
import logging
from decimal import Decimal

from app.services.dynamodb_service import DynamoDBService

logging.basicConfig(level=logging.INFO)

class ProductUseCases:
    def __init__(self, db_session: Session, dynamodb_service: DynamoDBService = None):
        self.db_session = db_session
        self.dynamodb_service = dynamodb_service
    
    def add_product(self, product: Product, category_slug: str):
        category = self.db_session.query(CategoryModel).filter_by(slug=category_slug).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Nao foi encontrada nenhuma categoria com esse slug')
        
        product_model = ProductModel(**product.dict())
        product_model.category_id = category.id

        self.db_session.add(product_model)
        self.db_session.commit()

    def update_product(self, id: int, product: Product):

        product_on_db = self.db_session.query(ProductModel).filter_by(id=id).first()

        if product_on_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nao foi encontrado produto com esse ID")
        
        product_on_db.name = product.name
        product_on_db.slug = product.slug
        product_on_db.price = product.price
        product_on_db.stock = product.stock

        self.db_session.commit()

    def proccess_csv_data(self, df, db_session):
        products = []
        for _, row in df.iterrows():
            if row['price'] < 0:
                raise ValueError(f"Price nao pode ser um valor negativo, {row['price']}")
            if row['stock'] < 0:
                raise ValueError(f"Stock nao pode ser um valor negativo, {row['stock']}")
            
            category = self.db_session.query(CategoryModel).filter_by(id=row['categoryid']).first()

            if category is None:
                raise ValueError(f"Categori nao encontrada, {row['categoryid']}")
            
            user = ProductModel(
                name=row['name'],
                slug=row['slug'],
                price=row['price'],
                stock=row['stock'],
                category_id = row['categoryid'],
                updated_at=datetime.now()
            )

            products.append(user)
            db_session.add(user)
        db_session.commit()
        self.__send_dynamo_db(products)

    def __send_dynamo_db(self, products):
        if not self.dynamodb_service:
            raise ValueError(f'Erro ao enviar produtos para o dynamodb pois a instancia de servico esta None')

        for product in products:
            try:
                item = {
                    'id': str(product.id),  # Certifique-se de que está usando a chave primária correta
                    'name': product.name,
                    'slug': product.slug,
                    'price': Decimal(str(product.price)),
                    'stock': Decimal(str(product.stock)),
                    'categoryId': str(product.category_id),
                    'updatedAt': product.updated_at.isoformat()
                }
                self.dynamodb_service.insert_item(item)
            except Exception as ex:
                raise ValueError(f'erro no envio dos dados ao servico do dynamo {ex}')