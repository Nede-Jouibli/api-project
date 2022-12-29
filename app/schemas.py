from pydantic import BaseModel, EmailStr #structure posts
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    issue: str
    challenge: str
    sector: str
    location: str
    published: bool = True

class PostCreate(PostBase):
    pass    

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


class PostResponse(PostBase):
    id: int
    created_at: datetime
    citizen_id: int
    citizen: CitizenInfo

    class Config:
        orm_mode =True    #convert the sqlalchemy to dict


class Token (BaseModel):
    access_token: str
    token_type: str    

class TokenData (BaseModel):
    id: Optional [str] = None