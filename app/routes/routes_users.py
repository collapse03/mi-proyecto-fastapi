from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException

from app.services.services_utils import services_utils
from ..database import get_user, update_user
from ..models.user_model import User
from ..services.services_login import services_login
from fastapi import UploadFile, File
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from pydrive.auth import GoogleAuth


router = APIRouter()
services_login_obj = services_login()
services_utils_obj = services_utils()

@router.get("/user")
def get_current_user(username: str = Depends(services_login_obj.decode_access_token)):
    user = get_user("username", username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return user

@router.put("/user")
def update_current_user(user: User, username: str = Depends(services_login_obj.decode_access_token)):
    existing_user = get_user("username", username)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_user(username, user.model_dump())
    return {"message": "User updated"}

@router.post("/user/photo")
async def upload_photo(photo: UploadFile = File(...), username: str = Depends(services_login_obj.decode_access_token)):

    temp_dir = "./temp"
    os.makedirs(temp_dir, exist_ok=True)  # Create the directory if it doesn't exist

    temp_file = os.path.join(temp_dir, photo.filename)

    drive = services_utils_obj.login_to_google_drive()
    try:
        # Use 'with' statement to ensure the file is closed properly
        with open(temp_file, "wb+") as buffer:
            buffer.write(await photo.read())
        
        file_drive = drive.CreateFile({'title': photo.filename})
        file_drive.SetContentFile(temp_file)  # Use the temporary file path
        file_drive.Upload()
        photo_url = file_drive['alternateLink']
        file_drive.content.close()
        update_user(username, {"photo": photo_url})

    except Exception as e:
        print(e)
    finally:
        # Delete the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return {"photo_url": "photo_url"}