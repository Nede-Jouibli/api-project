from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix="/issues", tags=['Issues'])

@router.get("/", response_model=List[schemas.IssueResponse])
def get_issues(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_citizen), 
               limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    
    #issues = db.query(models.Issue).filter(models.Issue.issue.contains(search)).limit(limit).offset(skip).all()
    issues = db.query(models.Issue).all()
    return issues  


@router.get("/{id}", response_model=schemas.IssueResponse) 
def get_issue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_citizen)): 

    issue = db.query(models.Issue).filter(models.Issue.id==id).first()
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with is: {id} was not found")
                            
    return issue


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.IssueResponse)
def post_issue(post: schemas.IssueCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_citizen)):

    new_post = models.Issue(citizen_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_citizen)):
    issue_query = db.query(models.Issue).filter(models.Issue.id==id)
    issue = issue_query.first()

    if issue == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Issue with id: {id} does not exist.")    
    if issue.citizen_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete this issue.")
    
    try:
        db.delete(issue)
        db.commit()
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting issue with id: {id}.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.IssueResponse)
def update_issue(id: int, updated_post:schemas.IssueCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_citizen)):

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