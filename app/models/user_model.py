from pydantic import BaseModel, EmailStr
from typing import Optional
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool
    email_confirmation: Optional[bool] = False

class Token(BaseModel):
    access_token: str
    token_type: str