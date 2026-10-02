from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import ollama_router

app = FastAPI()

# html=True 옵션 해주면 /로 접속했을 때 index.html을 찾아서 내려줌
app.mount("/frontend", StaticFiles(directory="frontend", html=True))

@app.get("/")
def index():
    return FileResponse("./frontend/index.html")

app.include_router(ollama_router.router)