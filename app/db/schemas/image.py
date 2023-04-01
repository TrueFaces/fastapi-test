from pydantic import BaseModel


class ImageBase(BaseModel):
    image_url: str
    thumbnail_url: str
    has_face: bool


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True