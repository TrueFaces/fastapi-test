from pydantic import BaseModel

# Images
class ImageBase(BaseModel):
    image_url: str
    thumbnail_url: str
    filesize: int
    filename: str
    has_face: bool
    has_avatar: bool
    is_avatar: bool


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Users
class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    images: list[Image] = []

    class Config:
        orm_mode = True

