from fastapi import FastAPI,APIRouter
from ..db.connection import get_db_connection
from typing import Optional

router = APIRouter(
    prefix='/api',
    tags=['API']
)
connection = get_db_connection()
cursor = connection.cursor()
@router.get('/')
def getAllProducts(limit:int = 20, offset:int = 0):
    cursor.execute(
        '''
            select product.id,product.name,price,available_items,product_category.name category,description from product inner join product_category 
            on product.product_category_id = product_category.id limit %s offset %s
        ''',(limit,offset)
    )
    items = cursor.fetchall()
    return {
        'message':'Success',
        'count':len(items),
        'items' : items
    }
    
@router.get('/search')
def search(query: str,limit:int = 20, offset:int = 0):
    statement = '''
        select product.id,product.name,price,available_items,product_category.name category,description from product inner join product_category 
        on product.product_category_id = product_category.id
        where product.name ilike %s
        or product_category.name ilike %s
        or description ilike %s
        limit %s offset %s
    '''
    cursor.execute(statement,(f"%{query}%",f"%{query}%",f"%{query}%",limit,offset))
    items = cursor.fetchall()
    return {
        'message':'Success',
        'count':len(items),
        'items' : items
    }
    