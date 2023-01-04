from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.responses import HTMLResponse
import hashlib
from datetime import datetime

router = APIRouter(prefix="/citizens", tags=['Citizens'])

@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.CitizenInfo)
def create_citizen(citizen: schemas.CreateCitizen, db: Session = Depends(get_db)):
    
    #hash the password
    hashed_pwd=utils.hash(citizen.password)
    citizen.password= hashed_pwd

    new_citizen = models.Citizen(**citizen.dict())
    db.add(new_citizen)
    db.commit()
    db.refresh(new_citizen)

    return new_citizen

@router.get('/{id}', response_model=schemas.CitizenInfo)
def get_citizen(id: int,  db: Session = Depends(get_db),):
    citizen = db.query(models.Citizen).filter(models.Citizen.id == id).first()

    if not citizen:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Citizen with id: {id} does not exist")
    return citizen                         


# #verification
# @router.get('/verification', response_model=HTMLResponse)
# async def citizen_email_verification(request: Request, token: str):
#     citizen = await oauth2.verify_access_token(token)

# @router.get('/verifyemail/{token}')
# def verify_me(token: str):
#     hashedCode = hashlib.sha256()
#     hashedCode.update(bytes.fromhex(token))
#     verification_code = hashedCode.hexdigest()
#     # result = User.find_one_and_update({"verification_code": verification_code}, {
#     #     "$set": {"verification_code": None, "verified": True, "updated_at": datetime.utcnow()}}, new=True)
#     # if not result:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code or account already verified')
#     return {
#         "status": "success",
#         "message": "Account verified successfully"
#     }