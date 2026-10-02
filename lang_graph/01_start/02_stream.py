from langchain_ollama import ChatOllama
from langgraph.constants import END
from langgraph.graph import StateGraph
from pydantic import BaseModel

# 1. 저장소 준비
class SimpleState(BaseModel):
    ori_q : str = ""
    refined_q : str = ""
    response: str = ""

# 2. LLM모델 준비
llm = ChatOllama(model = "gemma4:e4b")

# 3. 노드에 등록할 함수 준비
def refine_text_node(state: SimpleState) -> SimpleState:
    """유저의 질문을 따뜻한 문장으로 다듬는 노드"""
    prompt = f"""
    유저의 [질문]을 부드럽고 따뜻한 형태로 다듬어줘
    서문, 설명, 팁 등의 불필요한 내용은 제거하고 결과물 1개만 보여줘
    [질문]
    {state.ori_q}
    """

    res = llm.invoke(prompt)
    state.refined_q = res.content.strip()
    return state

def call_llm_node(state: SimpleState) -> SimpleState:
    """다듬어진 문장으로 최종 답변을 생성하는 노드"""
    res = llm.invoke(state.refined_q)
    state.response = res.content.strip()
    return state

# 4. 저장소 등록
wf = StateGraph(SimpleState)

# 5. 노드 등록
wf.add_node("refiner", refine_text_node)
wf.add_node("generator", call_llm_node)

# 6. 순서 지정
wf.set_entry_point("refiner")
wf.add_edge("refiner", "generator")
wf.add_edge("generator", END)

# 7. 컴파일
app = wf.compile()

# 8. 실행
query = input("아무거나 입력하세요\n")
for node in app.stream({"ori_q" : query}, stream_mode="updates"):
    for name, val in node.items(): # dic에서 키와 값을 쌍(entries)으로 뽑아낸다.
        print(f"{name} : {val}")