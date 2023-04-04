from sqlalchemy.orm import Session

from app.db.models import Image as ImageModel

def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ImageModel).offset(skip).limit(limit).all()

def get_image(db: Session, id: int):
    return db.query(ImageModel).filter(ImageModel.id == id).first()

def delete_image(db: Session, image):
    db.delete(image)
    db.commit() 