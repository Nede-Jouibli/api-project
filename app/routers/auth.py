from fastapi import APIRouter,Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi_jwt_auth import AuthJWT

router = APIRouter(tags=['Authentication']) 


#login of citizens
@router.post('/citizens/login', response_model=schemas.Token)
def login(info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
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
def login(info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    decisionmaker = db.query(models.DecisionMaker).filter(models.DecisionMaker.email==info.username).first()
    
    if not decisionmaker:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Login Information.")
    
    if not utils.verify(info.password, decisionmaker.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Login Information.")

    access_token = oauth2.create_access_token(data = {"user_id" : decisionmaker.id})
    refresh_token = oauth2.create_refresh_token(data = {"user_id" : decisionmaker.id})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type" : "bearer"}    


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
   
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}

@router.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}