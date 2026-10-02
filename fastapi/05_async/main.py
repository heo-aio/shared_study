import time
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

# /view라는 요청이 오면 view폴더로 이동
app.mount("/view", StaticFiles(directory="view"))

# CORS : Cross Origin Resource Sharing
# MiddleWare : 특정 라우트로 가기 전에 접근되는 곳(함수)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.get("/")
def main():
    return RedirectResponse("/view/index.html")

@app.get("/send")
def send(msg):
    print(f"msg = {msg}")
    time.sleep(5)
    return {"result" : f"보낸 메시지 - {msg}"}