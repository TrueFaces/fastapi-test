from sqlalchemy.orm import Session

from app.db.models import User as UserModel, Image as ImageModel
from app.db.schemas import ImageCreate, UserCreate
from app.internal.auth_utils import get_password_hash

def get_user(db: Session, user_id: int) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_images(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(ImageModel).join(UserModel).filter(UserModel.id == user_id).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(email=user.email, password=hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_image(db: Session, image: ImageCreate, user_id: int):
    db_image = ImageModel(user_id=user_id,
                          thumbnail_url=image.thumbnail_url, 
                          image_url = image.image_url,
                          filename=image.filename,
                          filesize=image.filesize )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
