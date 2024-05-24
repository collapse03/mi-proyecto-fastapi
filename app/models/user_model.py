from pydantic import BaseModel, EmailStr
from typing import Optional
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool
    email_confirmation: Optional[bool] = False
    name: Optional[str] = None
    lastName: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    photo: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str