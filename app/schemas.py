from pydantic import BaseModel, EmailStr #structure posts
from datetime import datetime
from typing import Optional


################## CitizenBase Model #################
class IssueBase(BaseModel):
    issue: str
    challenge: str
    sector: str
    location: str
    published: bool = True

class IssueCreate(IssueBase):
    pass    


################## Citizens #################
class CreateCitizen(BaseModel):
    email: EmailStr
    password: str   
    location: str     

class CitizenInfo(BaseModel):
    id: int
    email: EmailStr
    location: str   
    created_at: datetime
    
    class Config:
        orm_mode =True    #convert the sqlalchemy to dict


class CitizenLogin(BaseModel):
    email: EmailStr
    password: str 


class IssueResponse(IssueBase): #change this (postresponse)
    id: int
    created_at: datetime
    citizen_id: int
    citizen: CitizenInfo

    class Config:
        orm_mode =True    

################## Decision Makers #################   

################## DM Base Model #################
class FocusBase(BaseModel):
    issue_id: str
    status: str
    published: bool = True

class FocusCreate(FocusBase):
    pass    


class CreateDM(BaseModel):
    email: EmailStr
    password: str   
    organization: str     
    authority: str    

class DMInfo(BaseModel):
    id: int
    email: EmailStr
    organization: str     
    authority: str   
    created_at: datetime
    
    class Config:
        orm_mode =True   


class DMLogin(BaseModel):
    email: EmailStr
    password: str 

class IssueInfo(BaseModel):
    issue: str
    challenge: str
    sector: str
    location: str

    class Config:
        orm_mode =True 

        
class FocusResponse(FocusBase):
    id: int
    created_at: datetime
    decisionmaker_id: int
    decisionmaker: DMInfo
    issue: IssueInfo

    class Config:
        orm_mode =True    


################## Token ################# 
class Token (BaseModel):
    access_token: str
    refresh_token: str
    token_type: str    
    
class TokenData (BaseModel):
    id: Optional [str] = None

