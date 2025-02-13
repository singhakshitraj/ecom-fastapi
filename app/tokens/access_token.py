import jwt
from dotenv import load_dotenv
from ..statics.validations import UserSchema
import os
from datetime import datetime,timedelta
from fastapi import HTTPException,status,Depends
from ..statics.errors import error_as_dict
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer('login')

def generate_access_token(user:UserSchema):
    load_dotenv()
    pl = dict(user)
    token_expires_at = str(datetime.now()+timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))))
    pl.update({'expires':token_expires_at})
    token = jwt.encode(
        payload=pl,
        key=os.environ.get('SECRET_KEY'),
        algorithm=os.environ.get('ALGORITHM')
    )
    return token

def verify_access_token(token,exception):
    load_dotenv()
    data = jwt.decode(
        jwt=token,
        key=os.environ.get('SECRET_KEY'),
        algorithms=[os.environ.get('ALGORITHM')]
    )    
    username = data.get('username')
    if username is None:
        raise exception
    if str(datetime.now()) > data.get('expires'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=error_as_dict('Token Expired'))
    return username

def get_user(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=error_as_dict('Forbidden'))
    return verify_access_token(token,exception)