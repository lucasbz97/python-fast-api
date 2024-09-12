import boto3

class DynamoDBService:
    def __init__(self, region_name: str, table_name: str):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def insert_item(self, item: dict):
        try:
            self.table.put_item(Item=item)
        except Exception as ex:
            raise Exception(f"Ocorreu um erro no envio ao DynamoDb: {ex}")
