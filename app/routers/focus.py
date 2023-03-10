from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/focus_issue", tags=['Focus Issues'])

@router.get("/", response_model=List[schemas.FocusResponse])
def get_focus_issue(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_dm), 
               limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    
    #focus = db.query(models.Focus).filter(models.Focus.issue.contains(search)).limit(limit).offset(skip).all()
    focus = db.query(models.Focus).all()
    return focus 


@router.get("/{id}", response_model=schemas.FocusResponse) 
def get_focus_issue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_dm)): 

    focus= db.query(models.Focus).filter(models.Focus.id==id).first()
    if not focus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Focus with id: {id} was not found")
                            
    return focus


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.FocusResponse)
def post_focus_issue(post: schemas.FocusCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_dm)):

    new_focus = models.Focus(decisionmaker_id = current_user.id, **post.dict())
    db.add(new_focus)
    db.commit()
    db.refresh(new_focus)

    return new_focus


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_focus_issue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_dm)):
    focus_query = db.query(models.Focus).filter(models.Focus.id==id)
    focus = focus_query.first()

    if focus == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Focus with id: {id} does not exist.")    
    if focus.decisionmaker_id!= current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete this focus.")
    
    try:
        db.delete(focus)
        db.commit()
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting focus issue with id: {id}.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.FocusResponse)
def update_focus_issue(id: int, updated_post:schemas.FocusCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_dm)):

    focus_query = db.query(models.Focus).filter(models.Focus.id==id)
    focus=focus_query.first()

    if focus== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"focus with id: {id} does not exist")    
    
    if focus.decisionmaker_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update this focus issue.")

    focus_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    return focus_query.first()