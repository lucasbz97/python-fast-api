from io import StringIO
from fastapi import APIRouter, File, HTTPException, Response, Depends, UploadFile, status
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session, get_dynamo_db_service
from app.services.dynamodb_service import DynamoDBService
from app.use_cases.product import ProductUseCases
from app.schemas.product import ProductInput
from app.schemas.product import Product
import pandas as pd

router = APIRouter(prefix='/product', tags=['product'])

@router.post('/add')
def add_product(
    product_input: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    uc = ProductUseCases(db_session=db_session)
    uc.add_product(
        product=product_input.product,
        category_slug=product_input.category_slug
    )

    return Response(status_code=status.HTTP_201_CREATED)

@router.put('/update/{id}')
def update_product(
    id: int,
    product: Product,
    db_session: Session = Depends(get_db_session)
):
    uc = ProductUseCases(db_session=db_session)
    uc.update_product(id=id, product=product)

    return Response(status_code=status.HTTP_200_OK)

@router.post('/upload-csv')
async def upload_csv(file: UploadFile = File(...), 
                     db_session: Session = Depends(get_db_session), 
                     dynamodb_service: DynamoDBService = Depends(get_dynamo_db_service)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de arquivo inválido. Somente csv é aceito")
    
    contents = await file.read()
    csv_data = StringIO(contents.decode('utf-8'))

    try:
        df = pd.read_csv(csv_data)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro na leitura do arquivo CSV")
    
    required_columns = {'name', 'slug', 'price', 'stock', 'categoryid'}

    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="arquivo esta faltando colunas que são obrigatorias.\nColunas: name, slug, price, stock, categoryid")

    uc = ProductUseCases(db_session=db_session, dynamodb_service=dynamodb_service)
    uc.proccess_csv_data(df=df, db_session=db_session)

    return Response(status_code=status.HTTP_200_OK)