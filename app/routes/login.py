from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.services_login import services_login
from ..schemas.example_schema import Token
from fastapi import APIRouter
from ..database import get_user, add_user
from ..models.user_model import User

#CONFIGURATION VARIABLES

app = FastAPI()
router = APIRouter()

#ROUTES

@router.post("/login", response_model=Token)
def login_for_access_token(user: User):
    serivces_login = services_login()
    user_in_bd = serivces_login.authenticate_user(user.username, user.password)
    if not user_in_bd:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=serivces_login.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = serivces_login.create_access_token(
        data={"sub": user_in_bd["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
def register_user(user: User):
    if get_user(user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    add_user(user)
    return user