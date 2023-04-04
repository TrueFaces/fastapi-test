from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.repositories import images as imagesRepository
from app.db.schemas import Image
from app.db.database import get_db
from app.dependencies import oauth2_scheme

from app.internal.auth import get_current_user
from app.utils.storage import download_file_from_bucket

router = APIRouter(
    prefix="/images",
    tags=["images"],
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/", response_model=list[Image])
async def read_items(db: Session = Depends(get_db)):
    return imagesRepository.get_images(db=db)


@router.get("/{id}", response_model=Image)
async def read_item(id: str,  db: Session = Depends(get_db)):
    return imagesRepository.get_image(id=id, db=db)

@router.get("/{id}/download", response_model=None)
async def read_item(id: str,  
                    db: Session= Depends(get_db),
                    token: str = Depends(oauth2_scheme)):
    user = await get_current_user(db=db, token=token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    image = imagesRepository.get_image(id=id, db=db)

    return await download_file_from_bucket(user_id= user.id, filename=image.filename)

# @router.put("/{id}",responses=Image)
# async def update_image(id: str,  db: Session = Depends(get_db)):
#     image = imagesRepository.get_image(id=id, db=db)
#     if id is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     image
#     return imagesRepository.update_image(db: Session = Depends(get_db), image=image))
