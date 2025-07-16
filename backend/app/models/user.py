from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.shared import PyObjectId
from typing_extensions import Literal
from bson import ObjectId

# Public response schema
class UserPublic(BaseModel):
    id: Optional[PyObjectId] = None
    username: str
    email: EmailStr
    role: Literal["admin", "doctor", "patient"]

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}


# Schema for creating a user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["admin", "doctor", "patient"]


# Schema for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# For JWT token (if you're using authentication)
class Token(BaseModel):
    access_token: str
    token_type: str
