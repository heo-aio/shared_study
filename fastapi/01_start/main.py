# uv pip install fastapi uvicorn
# uvicorn main:app --host=0.0.0.0 --reload
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {"message": "안녕하세요 HeoJungMo입니다."}