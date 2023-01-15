from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/citizen", tags=['Citizens'])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.CitizenExist|schemas.CitizenInfo)
def create_citizen(citizen: schemas.CreateCitizen, db: Session = Depends(get_db)):

    existing_citizen = db.query(models.Citizen).filter(models.Citizen.email == citizen.email).first()

    if existing_citizen:
        return {"message": "Citizen with this email already exists, please try to log in instead."}
    
    else: 
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