from fastapi import FastAPI
from app.routes.login import router as login_router
from app.routes.routes_users import router as user_router
import uvicorn
app = FastAPI()

app.include_router(login_router, tags=["Login"], prefix="/login")
app.include_router(user_router, tags=["User"], prefix="/user")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)