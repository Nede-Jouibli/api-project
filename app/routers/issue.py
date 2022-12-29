from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=['Issues'])

@router.get("/", response_model=List[schemas.PostResponse])
def get_issues(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
               limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    
    issues = db.query(models.Issue).limit(limit).offset(skip).filter(models.Issue.issue.contains(search)).all()
    return issues  


@router.get("/{id}", response_model=schemas.PostResponse) #id is a path parameter
def get_issue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 

    post = db.query(models.Issue).filter(models.Issue.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with is: {id} was not found")
                            
    return {"post_detail": post}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def post_issue(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Issue(citizen_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Issue).filter(models.Issue.id==id)

    post = post_query.first()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")    

    if post.citizen_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete this issue.")
    
    post.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Issue).filter(models.Issue.id==id)
    post=post_query.first()

    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id: {id} does not exist")    
    
    if post.citizen_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update this issue.")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()