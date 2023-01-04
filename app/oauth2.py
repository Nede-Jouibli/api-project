from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def verify_access_token(token: str, info_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise info_exception
        token_data=schemas.TokenData(id = id)  

    except JWTError: 
        raise info_exception    

    return token_data

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#new
def verify_refresh_token(token: str, info_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise info_exception
        token_data=schemas.TokenData(id = id)  

    except JWTError: 
        raise info_exception    

    return token_data



def get_current_citizen(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):   
    info_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail=f"could not validate logging info.", 
                                   headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, info_exception)
    citizen = db.query(models.Citizen).filter(models.Citizen.id == token.id).first()
    return citizen


def get_current_dm(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):   
    info_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail=f"could not validate logging info.", 
                                   headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, info_exception)
    dm = db.query(models.DecisionMaker).filter(models.DecisionMaker.id == token.id).first()
    return dm
