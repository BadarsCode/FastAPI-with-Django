from passlib.context import CryptContext 
from jose import jwt 
from datetime import datetime, timedelta 
from fastapi.security import OAuth2PasswordBearer 


SECRET_KEY = "Mysecretkey"

ALGORITHM = 'HS256'

ACCESS_TOKEN_EXPIRE_MINUTES = 30 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 

# Decode jwt token

from jose import JWTError 


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )

        email: str = payload.get("sub")

        return email    
    except JWTError:
        return None

from fastapi import Depends, HTTPException
def get_current_user(
    token: str = Depends(oauth2_scheme)
    ):

    email = verify_token(token) 
    if not email: 
        raise HTTPException(status_code=401, detail = 'Invalid Token') 
    
    return email 