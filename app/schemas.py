from pydantic import BaseModel, EmailStr 
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

class CitizenExist(BaseModel):
    message: str


class IssueResponse(IssueBase): 
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

class DMExist(BaseModel):
    message: str


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


################## Tokens ################# 
class Token (BaseModel):
    access_token: str
    refresh_token: str
    token_type: str 


class NewToken (BaseModel): 
    new_access_token: str       
    
class TokenData (BaseModel):
    id: Optional [str] = None

class AuthJWT(BaseModel):
    access:str

class Authorize:
    def __init__(self,jwt:AuthJWT):
        self.jwt=jwt
    
    def jwt_refresh_token_required(self):
        return True