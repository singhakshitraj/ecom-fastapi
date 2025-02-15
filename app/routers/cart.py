from fastapi import APIRouter,Depends,HTTPException,status
from ..statics.validations import AddItemInCart,DeleteItemFromCart
from ..statics.errors import error_as_dict
from ..tokens.access_token import get_user
from ..db.connection import get_db_connection
router = APIRouter(
    prefix='/cart',
    tags=['Cart']
)

connection = get_db_connection()
cursor = connection.cursor()

@router.post('/add')
def add_item_to_cart(item:AddItemInCart,username = Depends(get_user)):
    cursor.execute(
        '''
            select available_items from product
            where id = %s
        ''',(item.product_id,)
    )
    total_available_item = cursor.fetchone()
    if total_available_item is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error_as_dict('No item found with this id'))
    if total_available_item.get('available_items') < item.itemcount:
        item_count = total_available_item.get('available_items')
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=error_as_dict(f'Only {item_count} available.'))
    try:
        cursor.execute(
            '''
                select * from user_cart
                where username = %s and product_id = %s
            ''',(username,item.product_id)
        )
        is_item_already_present = cursor.fetchone()
        if is_item_already_present:
            cursor.execute(
                '''
                    update user_cart
                    set itemcount = itemcount + %s
                    where username=%s and product_id=%s
                    returning *
                ''',(item.itemcount,username,item.product_id)
            )
        else:
            cursor.execute(
                '''
                    insert into user_cart (username,product_id,itemcount)
                    values 
                    (%s,%s,%s)
                    returning *
                ''',(username,item.product_id,item.itemcount)
            )
        new_item_in_cart = cursor.fetchone()
        cursor.execute(
            '''
                update product
                set available_items = %s
                where id = %s
            ''',( total_available_item.get('available_items')-item.itemcount,item.product_id)
        )
        connection.commit()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error_as_dict('Database Error!!'))
    return {
        'message' : 'Success',
        'item' : new_item_in_cart
    }
    
    
@router.post('/remove')
def remove_item_from_cart(item : DeleteItemFromCart , username = Depends(get_user)):
    cursor.execute(
        '''
            delete from user_cart
            where username = %s and product_id = %s
            returning *
        ''',(username,item.product_id)
    )
    deleted_item = cursor.fetchone()
    if deleted_item is None:
        return error_as_dict('No Corresponding Item in the Cart for this user')
    connection.commit()
    return {
        'message' : 'Successfully Deleted',
        'deleted_item' : deleted_item,
    }

@router.get('/items')
def get_cart_items(username = Depends(get_user)):
    cursor.execute(
        '''
            select * from user_cart
            where username = %s
        ''',(username,)
    )
    items_in_cart = cursor.fetchall()
    return {
        'status':'Success',
        'items' : items_in_cart
    }