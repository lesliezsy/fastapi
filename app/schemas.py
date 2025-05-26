# Pydantic is a data validation and settings management library for Python
from pydantic import BaseModel, EmailStr, conint, Field
from datetime import datetime
from typing import Optional, Union

# 1. validate the request body
# 2. convert the request body to a dictionary
# 3. store the request body in the payload variable
# 4. return the payload variable
# define the shape of the request body
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
        # this is to tell pydantic to use the ORM model
        # instead of the dict model
        # this is to convert the SQLAlchemy model to a Pydantic model


# decide which fields to include in the response
# this is to define the shape of the response body
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True
        # from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:  
        orm_mode = True
        # from_attributes = True
       

 
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # id: Optional[str] = None
    id: Union[str, int] = None

class Vote(BaseModel):
    post_id: int
    # dir: conint(le=1)
    dir: int = Field(..., le=1) 