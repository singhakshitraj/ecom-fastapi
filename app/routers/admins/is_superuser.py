from ...db.connection import get_db_connection


connection = get_db_connection()
cursor = connection.cursor()

def isSuperUser(username) -> bool:
    cursor.execute(
        '''
            select is_superuser from users
            where username = %s
        ''',(username,)
    )
    superuser_status = cursor.fetchone()
    return superuser_status.get('is_superuser')