from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": "world"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/uploadfile/")
async def create_upload_file(file: bytes = File(...)):
    return {"file_size": len(file)}