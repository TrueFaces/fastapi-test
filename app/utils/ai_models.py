from fastapi import UploadFile
import cv2
import numpy as np
from tensorflow.keras.models import load_model

def preprocess_image(contents: bytes):
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100, 100))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)

    return img

async def predict_has_face(file: UploadFile):
    contents = await file.read()
    img = preprocess_image(contents)

    # Hacer la predicción
    model = load_model("/app/app/models/modelo.h5")
    prediction = model.predict(img)
    print("------> prediction: ", prediction[0][0])

    # Devolver la predicción
    return prediction[0][0] > 0.5


async def predict_has_avatar(file: UploadFile):
    contents = await file.read()
    img = preprocess_image(contents)

    # Hacer la predicción contra el nuevo modelo
    # model = load_model("/app/app/models/modelo.h5")
    # prediction = model.predict(img)
    # print("------> prediction: ", prediction[0][0])

    # Devolver la predicción
    return False