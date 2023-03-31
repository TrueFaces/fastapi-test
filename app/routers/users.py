from fastapi import APIRouter

from app.db.schemas.user import User

router = APIRouter( prefix="/users",
    tags=["users"])

@router.get("/", response_model=list[User])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/{username}",  response_model=User)
async def read_user(username: str):
    return {"username": username}