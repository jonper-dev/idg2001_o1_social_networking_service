from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

#################################################################
### -- Pydantic models for request and response validation -- ###
#################################################################
## These models are used to validate the data sent to and from the API.

#############
### Users ###
#############
## Used for creating a new user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

## Used for updating a user (full update, PUT)
class UserUpdate(BaseModel):
    name: str
    email: str
    password: str

## Used for partial update (PATCH)
class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None



#############
### Posts ###
#############
## Used for creating a new post
class PostCreate(BaseModel):
    content: str
    reply_to_id: Optional[int] = None

## Used for updating a post (full update, PUT)
class PostUpdate(BaseModel):
    content: str
    reply_to_id: Optional[int] = None
    hashtags: Optional[list[str]] = []

## Used for a partial update (PATCH)
class PostPatch(BaseModel):
    content: Optional[str] = None
    reply_to_id: Optional[int] = None
    hashtags: Optional[list[str]] = []

## Used for detailed post-display, including user-information.
class PostOutput(BaseModel):
    id: int
    content: str
    timestamp: datetime
    user_id: int
    username: str
    likes: int
    is_liked_by_user: bool
    reply_to_username: Optional[str] = None

    class Config:
        orm_mode = True

## Like a post
class PostLike(BaseModel):
    user_id: int
    post_id: int

#############
### Login ###
#############
## Used for handling login requests.
class LoginInput(BaseModel):
    email: str
    password: str
    
    
    
#############
### Signup ###
#############
## Used for handling signup requests.    
class SignupInput(BaseModel):
    username: str
    email: EmailStr
    password: str
    
###########################
### Public User details ###
###########################
class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

##################
### Auth Satus ###
##################
# User logged in/not logged in        
class AuthStatus(BaseModel):
    authenticated: bool
    user: UserPublic