from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from agent_service import calc_tool

app = FastAPI()

app.mount("/view", StaticFiles(directory="view"))
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.get("/")
def main():
    return RedirectResponse(url="/view/index.html")

@app.get("/calc")
def calc(val1: str, oper: str, val2: str):
    # print(f"{val1} {oper} {val2}")
    prompt = f"a={val1}, b={val2} 일 경우 {val1} {oper} {val2}를 계산해줘"
    print(f"prompt = {prompt}")
    result = calc_tool(prompt)
    return {"result" : result}
