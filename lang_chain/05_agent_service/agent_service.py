import logging

from langchain.agents import create_agent
from langchain_core.tracers import langchain
from langchain_ollama import ChatOllama

from tools import check_weather, now_date, check_stock

logging.basicConfig(level=logging.INFO)
langchain.debug=True

# ollama 모델 생성
llm = ChatOllama(model="gemma4:e4b")

# 도구 등록
tools = [check_stock, check_weather, now_date]

# 시스템 명령
sys_prompt = """
당신은 도구를 사용할 수 있는 AI비서입니다.
질문에 답하기 위해서 필요하다면 도구를 활용해서 답변을 주세요.
[출력규칙]
1. 답변은 오직 한글로 해주세요
2. 문장에 '실시간 데이터가 아니다.' 'API가 필요하다.', '가정된 결과다' 같은 불필요한 주의사항(Note)
또는 추가설명은 붙이지마세요.
3. 도구를 활용한 결과는 오직 결과만 깔끔하게 한국어 문장으로 정리해서 답하세요.
"""

# 에이전트 생성
agent = create_agent(llm, tools=tools, system_prompt=sys_prompt)

def start_agent(query: str):
    # 프롬프트 생성 + 대답듣기
    # stream_mode = "updates" <-- 주요 과정이 종료될 때 마다 출력
    # stream_mode="messages" <-- default이고 기본(타이핑하듯이 출력)
    mode = "messages"
    for chunk in agent.stream({"messages":[("user", query)]}, stream_mode=mode):
        # print(chunk)
        # messages로 처리할 경우 chunk구조가 달라지므로 해당 내용으로 변경해줘야 한다.
        if mode == "updates" and "model" in chunk:
            message = chunk["model"]["messages"][-1].content
            yield message
        
        if mode == 'messages':
            # print(chunk[0])
            # 청크 객체 안에 tool_calls 라는 속성이 있으면
            # 있으면 AIMessage, 없으면 ToolMessage
            if hasattr(chunk[0],"tool_calls"):
                text = chunk[0].content
                if text != '':
                    yield text
