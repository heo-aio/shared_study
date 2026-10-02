from typing import Dict, Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, StreamingResponse
from starlette.staticfiles import StaticFiles

from ollama_service import chat_answer

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
# 한 번 mount시켜준 것에는 다른걸 걸어주면 안됨
app.mount("/view", StaticFiles(directory="view"))

@app.get("/")
def main():
    return RedirectResponse(url="/view/chat.html")

@app.post("/ask/chat")
def ask_chat(info: Dict[str, Any]):
    print(f"input : {info['question']}")

    return StreamingResponse(chat_answer(info['question']), media_type="text/plain")
