from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    thumbnail_url = Column(String)
    has_face = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))