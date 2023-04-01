from fastapi import Depends, FastAPI,  File, UploadFile
import uvicorn, os

## Add Doc Security
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.routers import images, users, auth
from app.db.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.include_router(auth.router)
app.include_router(users.router, dependencies=[Depends(oauth2_scheme)])
app.include_router(images.router, dependencies=[Depends(oauth2_scheme)])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to TrueFaces"}

@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation():
    return get_redoc_html(openapi_url="/openapi.json", title="docs")

## RUN!!!
# if __name__ == "__main__":
#     uvicorn.run(app, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0")