from fastapi import FastAPI
from app.routes.login import router as login_router
import uvicorn
app = FastAPI()

app.include_router(login_router, tags=["Login"], prefix="/login")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)