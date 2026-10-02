# uv pip install -r requirements.txt
import logging
import os
import shutil
import traceback
import uuid
from typing import List

from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, FileResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

# 일반 print 로그의 단점
# 로그가 찍힌 시간, 위치 등을 알 수 없음
# DEBUG > INFO > WARNING > ERROR > CRITICAL
logging.basicConfig(
    level=logging.INFO,
    format = "%(levelname)s:     [%(name)s] %(message)s - %(asctime)s]",
    datefmt = "%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

logger.info("logger test dadadadada")

FILE_PATH = "./upload"

# 특정 경로에 폴더 생성 (os 라이브러리 활용)
if not os.path.exists(FILE_PATH):
    os.mkdir(FILE_PATH)
    logger.info(f"{FILE_PATH}생성")

app.mount("/view", StaticFiles(directory="view"))
app.mount("/images", StaticFiles(directory=FILE_PATH))

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.get("/")
def main():
    return RedirectResponse(url="/view/upload.html")

@app.post('/upload')
# files는 UploadFile 객체들이 여러 개 담긴 리스트
def upload(files: List[UploadFile]):
    msg = "파일 업로드 실패"

    if not files or all(file.filename == "" for file in files):
        logger.warning("업로드된 파일이 없습니다.")
        return {"msg" : "업로드할 파일을 1개 이상 선택해주세요."}

    try:
        for file in files:
            logger.info(f"file name : {file.filename}") # img.png -> 1234567.png
            ori_filename = file.filename

            # 1. 파일명과 확장자 분리
            # name, ext = ori_filename.split('.') # .을 기준으로 나눔
            name, ext = os.path.splitext(ori_filename) # 확장자(ext)기준으로 나눔
            logger.info(f"파일이름 : {name} 확장자 : {ext}")

            # 2. 파일명 변경 + 3. 바꾼 파일명과 확장자 합치기
            new_filename = f"{uuid.uuid4()}{ext}"
            logger.info(f"new filename = {new_filename}")

            # 4. 파일 저장
            save_path = f"{FILE_PATH}/{new_filename}"
            # open() : 파일을 읽는 함수
            # w: write, r: read, b: binary, t: text, +: read & write
            # with : 자원을 사용한 후 로직이 종료되면 함께 닫아줌
            with open(save_path, "wb") as file_obj:
                shutil.copyfileobj(file.file, file_obj)


            msg = "파일 업로드 성공"
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc()) # 상세 에러로그 보기

    return {"msg" : msg}

@app.get("/files")
def files():
    # 특정 경로의 파일 리스트를 가져옴
    file_list = os.listdir(FILE_PATH)
    logger.info(file_list)
    return {"files" : file_list}

@app.get("/delete")
def delete(filename: str):
    path = f"{FILE_PATH}/{filename}"
    if os.path.exists(path):
        os.remove(path)
    return RedirectResponse(url="/view/file_list.html")

@app.get("/download")
def download(filename: str):
    path = f"{FILE_PATH}/{filename}"
    if os.path.exists(path):
        return FileResponse(path, media_type="application/octet=stream", filename=filename)
    else:
        return {"msg" : "해당 파일이 없습니다."}

