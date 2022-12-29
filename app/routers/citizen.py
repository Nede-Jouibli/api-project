from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

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