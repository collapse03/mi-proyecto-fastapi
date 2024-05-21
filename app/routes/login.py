from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import FastMail, MessageSchema
from app.services.services_login import services_login
from app.services.services_utils import services_utils
from ..schemas.example_schema import EmailSchema, Token
from fastapi import APIRouter
from ..database import get_user, add_user, update_user
from ..models.user_model import User
from itsdangerous import URLSafeTimedSerializer

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
    if user_in_bd["email_confirmation"] == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=serivces_login.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = serivces_login.create_access_token(
        data={"sub": user_in_bd["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(user: User):
    if get_user("username", user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if get_user("email", user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    add_user(user)
    obj_services_utils = services_utils()
    s = URLSafeTimedSerializer('your-secret-key')
    token = s.dumps(user.email, salt='email-confirmation')
    url = f'http://your-web-site.com/reset-password/{token}'
    await obj_services_utils.send_emails(subject="Email confirmation", 
                                        recipients=user.email, 
                                        body=f"Click on the link to confirm your email: {url}")
    return {"message": "User registered"}

@router.post("/password-recovery")
async def recover_password(email: EmailSchema):
    obj_services_utils = services_utils()
    s = URLSafeTimedSerializer('your-secret-key')
    user = get_user("email", email.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    token = s.dumps(email.email, salt='password-recovery')
    url = f'http://your-web-site.com/reset-password/{token}'
    await obj_services_utils.send_emails(subject="Password recovery", 
                                        recipients=email.email, 
                                        body=f"Click on the link to recover your password: {url}")
    return {"message": "Password recovery email sent"}

@router.get("/confirmation-email")
async def confirm_email(email: str):
    s = URLSafeTimedSerializer('your-secret-key')
    try:
        email = s.loads(email, salt='email-confirmation', max_age=3600)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
    
    user = get_user("email", email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    else:
        user["email_confirmation"] = True
        update_user(user["username"], user)

    return {"message": "Email confirmed"}