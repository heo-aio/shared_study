from typing import TypedDict, Annotated, Dict

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.constants import END
from langgraph.graph import add_messages, StateGraph


# 1. 상태 저장소 생성 : class를 Dictionary처럼 여기게 해줌
class AgentState(TypedDict):
    # Lang Graph에서는 상태를 덮어쓰는 것을 원칙으로 하고있다.
    # Annotated[데이터타입, 규칙]을 통해서 규칙을 변경한다.
    # 어노테이션(@) - 컴파일러에게 미리 힌트를 주는 개념
    #------------------------------------------------------------------
    # [LangGraph State 누적 설정]
    # LangGraph는 기본적으로 상태(State)를 반환할 때 기존 값을 '덮어쓰기'함.
    # 하지만 대화 기록(메시지)은 누적되어야 하므로,
    # Annotated와 add_messages를 통해 '덮어쓰기' 대신 '이어붙이기(누적)' 규칙을 적용함.
    messages: Annotated[list[BaseMessage], add_messages]


# 2. 모델 생성
llm = ChatOllama(model = "gemma4:e4b", temperature=0)

# 3. 툴 생성
@tool
def multiply(a: int, b: int) -> int:
    """
    두 정수를 곱하는 계산기 도구입니다. 곱셈이 필요할 때만 이 도굴르 사용하세요.

    Args:
        a: 첫 번째 정수
        b: 두 번째 정수
    """
    print(f"{a}*{b}를 구하는 도구 실행")

    return a * b

# 4. 툴 등록
# multiply 함수 객체 통째로 그대로 담아준 것
tools = [multiply]
model = llm.bind_tools(tools)

# 호출을 하기위한 등록
tools_dict = {} # {name:function} 저장하여 name을 부르면 해당 function이 나오도록
# 비어있는 딕셔너리(사전)를 만듭니다.

# 등록된 툴 목록(여기서는 [multiply] 하나가 들어있음)을 하나씩 꺼냅니다.
for tool in tools:
    # 딕셔너리에 키(이름)와 값(진짜 함수)을 쌍으로 저장합니다.
    # tool.name 은 "multiply" 라는 문자열이 되고,
    # tool 은 def multiply(...) 라는 실제 함수 객체가 됩니다.
    tools_dict[tool.name] = tool

# 5. 노드 및 라우터 함수 선언
def agent_node(state:AgentState) -> Dict:
    """사용자의 질문을 받아 응답하는 노드"""
    print("사용자 메시지를 받아서 분석중 ...")
    resp = model.invoke(state["messages"])
    print(f"[Agent Node]: {resp}]")
    return {"messages" : [resp]}

def tool_node(state:AgentState) -> Dict:
    """LLM의 요청에 따라서 필요한 툴을 실핸하는 노드"""
    # 메시지들 중에서 직전의(마지막) 메시지인 AIMessage를 가져온다.
    last_msg = state["messages"][-1]

    msg_list = []
    for call in last_msg.tool_calls:
        name = call["name"]
        args = call["args"]
        call_id = call["id"]
        print(f"id : {call_id} 실행")
        print(f"[Tool Node]     {name}({args})")
        func = tools_dict[name] # 함수를 꺼내온 다음
        result = func.invoke(args)   # 실행
        print(f"실행 결과 값 : {result}")
        msg_list.append(
            ToolMessage(content=str(result), tool_call_id=call_id)
        )

    return {"messages" : msg_list}

def should_continue(state:AgentState) -> str:
    """LLM 최근 메시지에서 tool_calls가 있으면 call_tool로, 아니면 go_end로 반환한다."""
    last_msg = state["messages"][-1]
    if len(last_msg.tool_calls) > 0:
        return "call_tool"
    else:
        return "go_end"

# 6. 노드 등록
wf = StateGraph(AgentState)
wf.add_node("agent", agent_node)
wf.add_node("tool", tool_node)

# 7. 엣지 조립
wf.set_entry_point("agent")
# wf.add_edge("agent", "tool")
# wf.add_edge("tool", END)
wf.add_conditional_edges(
    "agent",
    should_continue,
    {
        "call_tool" : "tool",
        "go_end" : END
    }
)
wf.add_edge("tool", "agent")

# 8. 컴파일
app = wf.compile()

# 9. 실행
q = input("아무거나 물어보세요\n")
for node in app.stream(
        {"messages":[HumanMessage(content=q)]},
                  stream_mode="updates"):
    for k, v in node.items():
        print(f"{k}: {v}")
"""
HumanMessage    : 사용자가 보내는 메시지(content)
AIMessage       : LLM모델이 생성한 메시지(content.tool_calls)
ToolMessage     : Tool이 수행 후 반환하는 메시지(content, tool_call_id)
"""
