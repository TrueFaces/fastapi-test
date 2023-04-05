from fastapi import APIRouter, HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session

from app.db.schemas import User, UserCreate
from app.db.schemas import Image, ImageCreate
from app.db.models import Image as ImageModel
from app.db.repositories import users as usersRepository
from app.db.database import get_db
from app.dependencies import oauth2_scheme

from app.internal.auth import get_current_user
from app.utils.storage import upload_file_to_bucket
import cv2
import numpy as np
from tensorflow.keras.models import load_model
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
async def upload_user_image(file: UploadFile,
                            db: Session = Depends(get_db),
                            token: str = Depends(oauth2_scheme)):

    user = await get_current_user(db=db, token=token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    file.filename = f"{int(time.time())}_{file.filename}"

    path = await upload_file_to_bucket(user.id, file)

    await file.seek(0)
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100, 100))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)

    # Hacer la predicción
    model = load_model("/app/app/models/modelo.h5")
    prediction = model.predict(img)

    # Devolver la predicción
    has_face = prediction[0][0] > 0.5
    print("------> prediction: ", prediction[0][0])

    image = ImageCreate(image_url=path,
                        thumbnail_url=path,
                        filesize=file.size,
                        filename=file.filename,
                        has_face=has_face)
    return usersRepository.create_user_image(db=db,
                                             image=image,
                                             user_id=user.id)


# Ruta para realizar las predicciones a partir de un archivo
@router.post("/predict", response_model=PredictionSchema)
async def predict(file: UploadFile,
                  db: Session = Depends(get_db),
                  token: str = Depends(oauth2_scheme)):
    # Cargar imagen y aplicar preprocesamiento
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100, 100))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)

    # Hacer la predicción
    model = load_model("/app/app/models/modelo.h5")
    prediction = model.predict(img)

    # Devolver la predicción
    if prediction[0][0] > 0.5:
        face = "La imagen es una cara."
    else:
        face = "La imagen no es una cara."

    # Devolver la lista de caras detectadas

    return PredictionSchema(filename=file.filename,
                            content_type=file.content_type,
                            prediction=face)
