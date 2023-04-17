from sqlalchemy.orm import Session

from app.db.models import Image as ImageModel

def get_images(db: Session,  user_id: int, skip: int = 0, limit: int = 100):
    return db.query(ImageModel).filter(ImageModel.user_id == user_id).offset(skip).limit(limit).all()

def get_image(db: Session, user_id: int, id: int):
    return db.query(ImageModel).filter(ImageModel.id == id).filter(ImageModel.user_id == user_id).first()

def delete_image(db: Session, image):
    db.delete(image)
    db.commit() 