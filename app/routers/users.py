from fastapi import APIRouter, HTTPException, Depends, UploadFile, Request
from sqlalchemy.orm import Session

from app.db.schemas import User, UserCreate
from app.db.schemas import Image, ImageCreate
from app.db.models import Image as ImageModel
from app.db.repositories import users as usersRepository
from app.db.repositories import images as imagesRepository
from app.db.database import get_db
from app.dependencies import oauth2_scheme

from app.internal.auth import get_current_user
from app.utils.storage import upload_file_to_bucket, delete_file_from_bucket
from app.utils.ai_models import predict_has_face
from app.utils.request import get_domain
from pydantic import BaseModel
import time

router = APIRouter(prefix="/users", tags=["users"])


class PredictionSchema(BaseModel):
    filename: str
    content_type: str
    prediction: str


@router.get("/", response_model=User)
async def get_current_user_data(db: Session = Depends(get_db),
                                token: str = Depends(oauth2_scheme)):
    user = await get_current_user(db=db, token=token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# @router.get("/{email}", response_model=User)
# async def read_user(email: str,  db: Session = Depends(get_db)):
#     db_user = usersRepository.get_user_by_email(db=db, email=email)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@router.get("/images", response_model=list[Image])
async def get_user_images(db: Session = Depends(get_db),
                          token: str = Depends(oauth2_scheme)):
    user = await get_current_user(db=db, token=token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return usersRepository.get_images(db=db, user_id=user.id)


@router.post("/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = usersRepository.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return usersRepository.create_user(db=db, user=user)


@router.post("/upload", response_model=Image)
async def upload_avatar_image(file: UploadFile,
                              request: Request,
                            db: Session = Depends(get_db),
                            token: str = Depends(oauth2_scheme)):

    user = await get_current_user(db=db, token=token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    avatar = usersRepository.get_avatar(db=db, user_id=user.id)
    if avatar is None:
        file.filename = f"{int(time.time())}_{file.filename}"
        
        # Check if got face
        has_face = await predict_has_face(file)
        
        if has_face:
            path = await upload_file_to_bucket(user.id, file)
            image = ImageCreate(image_url=path,
                            thumbnail_url=path,
                            filesize=file.size,
                            filename=file.filename,
                            is_avatar = True,
                            has_avatar = True,
                            has_face=has_face)
            return usersRepository.create_user_image(db=db,
                                                image=image,
                                                user_id=user.id,
                                                domain=get_domain(request))
        else:
            raise HTTPException(status_code=400, detail="Image could not be avatar because it has'nt got a face") 

    else:
        raise HTTPException(status_code=400, detail="You've got one avatar uploaded. Delete first to upload new one") 

@router.delete("/removeAvatar")
async def remove_avatar_image(db: Session = Depends(get_db),
                            token: str = Depends(oauth2_scheme)):
    user = await get_current_user(db=db, token=token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    avatar = usersRepository.get_avatar(db=db, user_id=user.id)
    if avatar is None:
        raise HTTPException(status_code=404, detail="User does not have avatar")
    
    await delete_file_from_bucket(user_id=user.id, filename=avatar.filename)
    imagesRepository.delete_image(db=db,image=avatar)
    
    return {"status": "ok"}
    

# Ruta para realizar las predicciones a partir de un archivo
@router.post("/predict", response_model=PredictionSchema)
async def predict(file: UploadFile):
    # Cargar imagen y aplicar preprocesamiento
    prediction = predict_has_face(file)

    # Devolver la predicción
    if prediction[0][0] > 0.01:
        face = "La imagen es una cara."
    else:
        face = "La imagen no es una cara."

    # Devolver la lista de caras detectadas

    return PredictionSchema(filename=file.filename,
                            content_type=file.content_type,
                            prediction=face)
