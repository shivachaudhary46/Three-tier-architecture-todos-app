from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy import select
import jwt
from jwt.exceptions import InvalidTokenError
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy.orm import Session
load_dotenv()
from typing import Union, Annotated

from database import get_db, User, hasher
from schemas import TokenData 

from config import settings

'''
get important environment variables from .env file, using load_dotenv()
'''
secret_key = os.getenv("secret_key")
ALGO = os.getenv("ALGO")

'''
This will create sleek looking authorize and authentication which will 
take the username, password with the password bearer token, 
Header -> must be added with bearer + application/json, and we can access 
with OAuth2PasswordRequestForm
'''
oauth_scheme2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

'''
to get username from the database, it is necessary function to extract
username and dump in to the UserInDB class. 
'''
def get_user(username: str, DB: Session = Depends(get_db)) -> User:
    statement = select(User).where(User.username == username)
    result = DB.execute(statement)
    return result.scalar_one_or_none()


'''
first, we will try to read the username from the database
second, verify the password. remember we have done hashing of the password, to store
so we need to verify by using the PasswordHash.recommended(), we need to pass plain_password, 
and hashed password as argument. 
'''
def authenticate_user(username: str, password: str, DB: Session = Depends(get_db)) :
    user = get_user(username, DB)

    if not user:
        return None
    if not isinstance(password, str):
        return none
    if not hasher.verify(password, user.password_hash):
        return None 
    return user

'''
we can create a token with the jwt, the dict data will look like this which 
will later converted into the json web tokens, 
data = {
    "sub": "user.username",
    "exp": timedelta(minutes=??),  ## this will determine the token expirity
}
Create access token 
'''

def create_access_token(data: dict, expire_time: Union[timedelta, None] = None):
    to_encode = data.copy()
    
    if expire_time:
        expire = datetime.now(timezone.utc) + expire_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    # Add validation
    if not settings.SECRET_KEY:
        raise ValueError("SECRET_KEY is not configured")
    
    encoded_jwt = jwt.encode(
        to_encode, 
        str(settings.SECRET_KEY),  # Ensure it's a string
        algorithm=settings.ALGO
    )
    return encoded_jwt

'''
We can look if the user has token expirity remaining or not, we can do by using, 
jwt.decode() with secret key and algorithm, and we can access the username, and 
extract that user from the database.  
'''
async def get_current_user(token: Annotated[str, Depends(oauth_scheme2)], DB: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Use SECRET_KEY (uppercase) - same as in create_access_token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGO])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username, DB=DB)
    if user is None:
        raise credentials_exception
    return user
