from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str