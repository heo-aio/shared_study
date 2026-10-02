from typing import Dict

from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from starlette.responses import StreamingResponse

router = APIRouter(prefix="/ask", tags=["ask"])

model = ChatOllama(model="exaone3.5:2.4b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 어려운 기술을 알기 쉽게 설명해주는 전문가야"),
    ("user", "{topic}에 대해서 설명해줘")
])

# q = input("질문 내용을 입력하세요.\n")

@router.post("/stream")
def get_answer(info:Dict[str, str]):
    # content 부분은 지속적으로 데이터를 줘야함
    # return은 여러번 불가능
    # StreamingResponse안에서 지속적으로 실행하며 데이터를 줄 함수가 필요함
    return StreamingResponse(output_str(info['q']), media_type="text/plain")

def output_str(q):
    chain = prompt | model | StrOutputParser()

    for chunk in chain.stream({"topic" : q}):
        # print(chunk, end="", flush=True)
        yield chunk # return 후 완전히 종료된게 아니면 대기



