# ollama model 확인방법
# 1. huggingface.co에서 App이 ollama이거나 파일 뒤 GGUF가 묻은 모델 사용
# 2. ollama.com/search
from typing import Dict, Any

from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# ask라는 요청이 들어오면 불러와라
router = APIRouter(prefix="/ask", tags=["ask"])

# 모델 생성
model = ChatOllama(
    model = "exaone3.5:2.4b",
)

# 프롬프트 틀 제작 (system and user)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 쉽게 정보를 전달해주는 AI 분야 전문가입니다. 알기 쉽게 예시를 주면서 설명하세요"),
    ("user", "{topic}에 대해서 설명해주세요.")
])

@router.post("/batch") # /ask/batch
# Any = 어떤 것이든 올 수 있다. (현재 key = str value = Any)
def get_answer(info:Dict[str, Any]): # post로 받을 땐 단일 변수로 받을 수 없다. (dict or class)
    # 파이프라인 조립 LCEL(Lang Chain Express Language)
    # StrOutputParser를 안써도 답은 받을 수 있는데, 안쓰면 타이핑이 좀 늘어남
    chain = prompt | model | StrOutputParser()

    # 추론 실행
    # query = input("질문 내용을 입력하세요.\n")
    query = info['q']
    answer = chain.invoke({"topic" : query})
    return {"answer" : answer}


