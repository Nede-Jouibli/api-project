from fastapi import APIRouter,Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
import jwt


router = APIRouter(tags=['Authentication']) 


#login of citizens
@router.post('/citizens/login', response_model=schemas.Token)
def citizen_login(info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    citizen = db.query(models.Citizen).filter(models.Citizen.email==info.username).first()
    
    if not citizen:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Login Information.")
    
    if not utils.verify(info.password, citizen.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Login Information.")

    access_token = oauth2.create_access_token(data = {"user_id" : citizen.id})
    refresh_token = oauth2.create_refresh_token(data = {"user_id" : citizen.id})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type" : "bearer"}    



#login of decision makers
@router.post('/decisionmakers/login', response_model=schemas.Token)
def decisionmaker_login(info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    decisionmaker = db.query(models.DecisionMaker).filter(models.DecisionMaker.email==info.username).first()
    
    if not decisionmaker:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Login Information.")
    
    if not utils.verify(info.password, decisionmaker.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Login Information.")

    access_token = oauth2.create_access_token(data = {"user_id" : decisionmaker.id})
    refresh_token = oauth2.create_refresh_token(data = {"user_id" : decisionmaker.id})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type" : "bearer"}    

@router.get("/refresh")
def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, oauth2.SECRET_KEY, algorithms=[oauth2.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
    except oauth2.JWTError:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    
    new_access_token = oauth2.create_access_token({"user_id": user_id})
    return {"access_token": new_access_token}

