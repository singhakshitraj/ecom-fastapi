from fastapi import APIRouter,Depends,HTTPException,status
from .validations import addProduct,deleteProduct
from ...tokens.access_token import get_user
from ...db.connection import get_db_connection
from ...statics.errors import error_as_dict
from .is_superuser import isSuperUser

connection = get_db_connection()
cursor = connection.cursor()

product_router = APIRouter(
    prefix='/products',
)

@product_router.post('/add')
def addProducts(product:addProduct,username = Depends(get_user)):
    is_superuser = isSuperUser(username)
    if is_superuser is None or not is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=error_as_dict('You are not a superuser'))
    command = '''
        insert into product (name,product_category_id,price,available_items)
        values (%s,%s,%s,%s)
        returning *
    '''
    cursor.execute(query=command,vars=(product.name,product.product_category_id,product.price,product.available_items))
    added_item = cursor.fetchone()
    connection.commit()
    return {
        'status' : "Success",
        'item' : added_item
    }
    
@product_router.delete('/delete')
def deleteProducts(product : deleteProduct,username = Depends(get_user)):
    is_superuser = isSuperUser(username=username)
    if is_superuser is None or not is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=error_as_dict('You are not a superuser'))
    is_product_present = '''
        select * from product
        where id = %s
    '''
    cursor.execute(is_product_present,(product.id,))
    item = cursor.fetchone()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=error_as_dict('No Item found with this id'))
    delete_command = '''
        delete from product
        where id = %s
    '''
    try:
        cursor.execute(delete_command,(product.id,))
        connection.commit()
        return {
            'status' : 'Success',
            'deleted_post_id' : product.id  
        }
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error_as_dict('The item that is being deleted has been ordered by people in the past.'))