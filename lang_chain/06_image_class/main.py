import os.path

from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from image_service import file_Upload, class_img

IMG_PATH = "./upload/"

app = FastAPI()

app.mount("/view", StaticFiles(directory="view"))

if not os.path.exists(IMG_PATH):
    os.mkdir(IMG_PATH)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.get("/")
def index():
    return RedirectResponse(url="./view/upload.html")

@app.post("/upload")
def upload(files: UploadFile):
    save_path = f"{IMG_PATH}/{files.filename}"
    msg = "file upload failed"
    success = file_Upload(files.file, save_path)
    result = None
    if success == 1:
        msg = "file upload success"
        result = class_img(save_path)

    return {"upload": msg, "image": files.filename, "result": result}



