from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str  
    phone_number:str
    
class UserResponce(BaseModel):
    id:int
    username:str
    email:EmailStr  
    created_at:datetime
    #pydantic models takes only dict as valid input 
    #To convert sqlalchemy model into pydantic model
    class Config:
        orm_mode = True

class PostBase(BaseModel):                     # Schema for Request
    title:str
    content:str
    published:bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class PostResponce(PostBase):                     # Schema for Responce
    id:int 
    created_at:datetime
    owner_id:int 
    owner: UserResponce
    #pydantic models takes only dict as valid input 
    #To convert sqlalchemy model into pydantic model
    class Config:
        orm_mode = True

class PostResponceVote(BaseModel):
    Post:PostResponce
    votes:int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr 
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0,lt=2)