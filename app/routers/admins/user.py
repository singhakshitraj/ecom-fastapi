from fastapi import HTTPException,APIRouter,Depends,status,Response
from .validations import addSuperUserValidation
from ...tokens.access_token import get_user
from ...db.connection import get_db_connection
from ...statics.errors import error_as_dict

router = APIRouter(
    prefix='/users',
    tags=['Admin','Users']
)

connection = get_db_connection()
cursor = connection.cursor()

@router.post('/addsuperuser',status_code=status.HTTP_201_CREATED)
def addSuperUser(user_to_add:addSuperUserValidation , username = Depends(get_user)):
    cursor.execute(
        '''
            select * from users
            where username = %s
        ''',(user_to_add.username,)
    )
    user_to_super = cursor.fetchone()
    if user_to_super is None:
        raise HTTPException( status_code = status.HTTP_400_BAD_REQUEST,detail=error_as_dict('The User supplied is not valid'))
    is_current_user_super = '''
        select * from users
        where username = %s
    '''
    cursor.execute(is_current_user_super,(username,))
    current_user = cursor.fetchone()
    print(current_user)
    if not current_user['is_superuser']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=error_as_dict('Logged in user is not superuser'))
    if user_to_super['is_superuser']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error_as_dict('Already A superuser'))
    try:
        cursor.execute(
            '''
                update users
                set is_superuser = True
                where username = %s
            ''',(user_to_add.username,)
        )
        connection.commit()
    except Exception as error:
        raise error
    return {
        'status' : 'Success',
        'user' : user_to_add.username,
        'role' : 'superuser'
    }