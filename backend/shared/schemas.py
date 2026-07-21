from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# note
class NoteBase(BaseModel): 
    title: str

class NoteRead(NoteBase): 
    id: int
    user_id: int 
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NoteDelete(BaseModel): 
    id: int 

class NoteUpdate(NoteDelete): 
    title: Optional[str] = None 

# user
class UserBase(BaseModel): 
    username: str 
    email: EmailStr

class UserCreate(UserBase): 
    password: str 

class UserUpdate(BaseModel): 
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None 

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int 
    created_at: datetime

class UserReadWithNotes(UserRead): 
    notes: List[NoteRead] = []

class Token(BaseModel): 
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    username: str
