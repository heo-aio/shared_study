from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from starlette.responses import RedirectResponse

from review_model import ReviewAnalysis

app = FastAPI()

@app.get("/")
def main():
    return RedirectResponse(url="/docs")

# ollama model 호출
model = ChatOllama(model = "exaone3.5:2.4b")

# 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages([
    ("system", "넌 리뷰 분석가야. 리뷰를 분석해서 지정된 형식으로 답변줘"),
    ("human", "리뷰 : {review}")
])

# 출력 구조화 선언
structured_model = model.with_structured_output(ReviewAnalysis)

@app.get("/review/analysis")
def get_structured(review:str):
    # 파이프라인 조립
    chain = prompt | structured_model

    # 출력
    result = chain.invoke({"review" : review})
    print(result)
    # 일반적일 땐, model_dump() / 보내는 내용이 복잡하면 model_dump_json()
    # return result.model_dump_json() # json형태의 문자열(받는쪽에서 JSON.parse() 써줘야한다)
    return result.model_dump() # dict형태로 변환 -> FastAPI에선 dict로 반환하면 json으로 자동 변환