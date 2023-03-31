from pydantic import BaseModel

from app.db.schemas.image import Image

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    images: list[Image] = []

    class Config:
        orm_mode = True