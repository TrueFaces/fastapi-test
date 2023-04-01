from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from google.cloud import storage

from app.db.schemas.image import Image

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}



@router.get("/", response_model=list[Image])
async def read_items():
    return fake_items_db


@router.get("/{item_id}", response_model=Image)
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


# @router.put(
#     "/{item_id}",
#     tags=["custom"],
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}


@router.post("/upload/", response_model=Image)
async def create_upload_file(file: UploadFile):
    # upload_file_to_bucket("", "data/user/1/" + file.filename, file)
    return {"file_size": file.size, "filename": file.filename}
    
def upload_file_to_bucket(bucket_name, blob_name, file):
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your new GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Mode can be specified as wb/rb for bytes mode.
    # See: https://docs.python.org/3/library/io.html
    with blob.open("w") as f:
        f.write(file)