import os

DYNAMODB_CONFIG = {
    'region_name': os.getenv('DYNAMODB_REGION', 'us-east-1'),
    'table_name': os.getenv('DYNAMODB_TABLE', 'products')
}