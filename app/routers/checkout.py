from fastapi import APIRouter,Depends,HTTPException,status
from ..tokens.access_token import get_user
from ..db.connection import get_db_connection
from ..statics.errors import error_as_dict
import uuid
from ..statics.payment import payment

router = APIRouter(
    tags=['Final Checkout']
)
connection = get_db_connection()
cursor = connection.cursor()

@router.get('/checkout')
def checkout(username = Depends(get_user)):
    cursor.execute(
        '''
            select * from user_cart inner join product on user_cart.product_id = product.id
            where username = %s
        ''',(username,)
    )
    items_in_cart = cursor.fetchall()
    if items_in_cart is None or len(items_in_cart) == 0:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=error_as_dict('No items in cart.'))
    query = '''
        insert into order_details(order_id,username,product_id,itemcount)
        values
        (%s,%s,%s,%s)
    '''
    order_id = str(uuid.uuid4())
    values = []
    total_sum = 0
    for item in items_in_cart:
        total_sum += item["itemcount"] * item["price"]
        values.append((order_id,username,item["product_id"],item["itemcount"]))
    try:
        payment_status_or_id = payment(order_id=order_id,total_sum=total_sum)
        if not payment_status_or_id:
            raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,detail=error_as_dict('Payment Operation Failed'))
        cursor.executemany(query,values)
        cursor.execute(
        '''
            delete from user_cart
            where username = %s
        ''',(username,))
        connection.commit()
    except Exception as error:
        raise error
    return {
        'status' : 'Success',
        'payment' : 'Done',
        'payment_id' : payment_status_or_id
    }