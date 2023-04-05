from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from google.cloud import storage
import io

from fastapi.security import OAuth2PasswordBearer
from fastapi.logger import logger

from app.config import settings

ROOT_PATH = "data/user"


async def upload_file_to_bucket(user_id: int, file: UploadFile):
    file_path = f'{ROOT_PATH}/{user_id}/{file.filename}'

    storage_client = storage.Client()
    bucket = storage_client.bucket(settings.bucket)

    blob = bucket.blob(file_path)
    blob.upload_from_file(file.file)

    return blob.public_url


async def download_file_from_bucket(user_id: int, filename: str):
    file_path = f'{ROOT_PATH}/{user_id}/{filename}'

    storage_client = storage.Client()
    bucket = storage_client.bucket(settings.bucket)

    blob = bucket.blob(file_path)

    file_stream = io.BytesIO()
    blob.download_to_file(file_stream)
    file_stream.seek(0)

    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"})


async def delete_file_from_bucket(user_id: int, filename: str):
    file_path = f'{ROOT_PATH}/{user_id}/{filename}'

    storage_client = storage.Client()
    bucket = storage_client.bucket(settings.bucket)

    blob = bucket.blob(file_path)
    # Check if file exists
    blob.delete()
