from fastapi import Depends
from app.config import DYNAMODB_CONFIG
from app.db.connections import Session
from app.services.dynamodb_service import DynamoDBService

def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

def get_dynamo_db_service() -> DynamoDBService:
    return DynamoDBService (
        region_name=DYNAMODB_CONFIG['region_name'],
        table_name=DYNAMODB_CONFIG['table_name'],
    )
    