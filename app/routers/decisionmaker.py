from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/decisionmaker", tags=['Decision Makers'])

@router.post("/signup", status_code=status.HTTP_201_CREATED,  response_model=schemas.DMExist|schemas.DMInfo)
def create_decisionmaker(decisionmaker: schemas.CreateDM, db: Session = Depends(get_db)):

    existing_decisionmaker = db.query(models.DecisionMaker).filter(models.DecisionMaker.email == decisionmaker.email).first()

    if existing_decisionmaker:
        return {"message": "Decision Maker with this email already exists, please try to log in instead."}
    
    else:
        hashed_pwd=utils.hash(decisionmaker.password)
        decisionmaker.password= hashed_pwd

        new_decisionmaker = models.DecisionMaker(**decisionmaker.dict())
        db.add(new_decisionmaker)
        db.commit()
        db.refresh(new_decisionmaker)

        return new_decisionmaker

@router.get('/{id}', response_model=schemas.DMInfo)
def get_decisionmaker(id: int,  db: Session = Depends(get_db),):
    decisionmaker = db.query(models.DecisionMaker).filter(models.DecisionMaker.id == id).first()

    if not decisionmaker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Decision Maker with id: {id} does not exist")
    return decisionmaker                        