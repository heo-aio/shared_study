import logging

import langchain
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from tools import plus, minus, multiply, divide

# 추론과정을 확인하기 위한 로그 설정
logging.basicConfig(level=logging.INFO)
langchain.debug = True

# 모델 불러오기
# ollama run gemma4:e4b
model_id = "gemma4:e4b"
model = ChatOllama(model=model_id, temperature=0)

# 도구 등록
tools = [plus, minus, multiply, divide]

# 에이전트 생성
agent = create_agent(model=model, tools=tools)

# 프롬프트 제작
# 3+3은?
# a = 5, b = 10일 경우 a + b를 계산해줘
# msg = input("사칙 연산을 해보세요~~ 예) 3 + 3\n")
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 사칙연산 전문가입니다. 값 a와 b 연산자가 주어지면 연산 후 결과를 말해줍니다"),
    ("user", "{message}")
])

def calc_tool(msg):
    # 파이프라인 조합
    chain = prompt | agent

    # 실행
    response = chain.invoke({"message" : msg})

    print("=== AI의 생각 과정 및 도구 실행 모니터링 ===")
    for idx, msg in enumerate(response["messages"]):
        print(f"[STEP]{idx}     {msg}")

    return response["messages"][-1].content

