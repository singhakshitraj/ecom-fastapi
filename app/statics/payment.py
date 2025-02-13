from ..db.connection import get_db_connection

connection = get_db_connection()
cursor = connection.cursor()
def payment(order_id : str,total_sum :int) -> bool:
    is_payment_done = True # in future, True will be replaced by payment(parameters)->bool
    if is_payment_done:
        cursor.execute(
            '''
                insert into payment_details(order_id,amount)
                values(%s,%s)
                returning *
            ''',(order_id,total_sum)
        )
        payment_details = cursor.fetchone()
        return payment_details.get('order_id')
    else:
        return False