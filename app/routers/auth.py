from fastapi import FastAPI,APIRouter,HTTPException,status
from ..statics.validations import UserSchema
from ..db import connection
from ..statics.errors import error_as_dict
from ..statics.password_hash import PasswordProtector
from ..tokens import access_token


router = APIRouter(
    prefix='/u',
    tags=['Authentication']
)

conn = connection.get_db_connection()
cursor = conn.cursor()

@router.post('/login')
def login_(user : UserSchema):
    try:
        cursor.execute(
            '''
                select * from users
                where username = %s
            ''',(user.username,)
        )
        user_in_db = cursor.fetchone()
        if user_in_db is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=error_as_dict('No User Found with this particular username'))
        if not PasswordProtector.verifyPassword(user.password,user_in_db.get('password')):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=error_as_dict('Incorrect Password'))
        token = access_token.generate_access_token(user=user)
    except Exception as error:
        raise error
    return {
        'status' : 'Success',
        'username' : user.username,
        'access_token' : token
    }

@router.post('/register')
def register_(user:UserSchema):
    try:
        cursor.execute(
            '''
                select * from users
                where username=  %s
            ''',(user.username,)
        )
        user_in_db = cursor.fetchone()
        if user_in_db is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=error_as_dict('User already Exists. Try Login.'))
        cursor.execute(
            '''
                insert into users(username,password)
                values(%s,%s)
                returning *
            ''',(user.username,PasswordProtector.hashPassword(user.password))
        )
        registered_user = cursor.fetchone()
        if registered_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=error_as_dict('Server Problem'))
        conn.commit()
    except Exception as exceptions:
        raise exceptions
    return login_(user)
    