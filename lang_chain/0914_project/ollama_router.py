from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from starlette.responses import StreamingResponse

from schema import DiaryEntry

router = APIRouter(prefix="/api", tags=["api"])

model = ChatOllama(
    model = "gemma4:e4b"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """당신은 다정한 감정일기 분석가입니다.
사용자의 일기를 읽고 반드시 아래 형식으로만 답하세요. 다른 말은 절대 덧붙이지 마세요.

[감정 단어 하나]
---
[일기 내용에 공감하는 한두 문장의 코멘트]

감정 단어는 반드시 다음 중 하나여야 합니다: 기쁨, 평온, 슬픔, 불안, 지침"""),
    ("human", "{text}")
])

chain = prompt | model

@router.post("/analyze")
def analyze(info: DiaryEntry):
    print(f"input : {info.text}")
    def generate():
        for chunk in chain.stream({"입력 text": info.text}):
            yield chunk.content

    return StreamingResponse(generate(), media_type="text/plain")