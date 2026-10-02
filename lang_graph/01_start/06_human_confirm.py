# 1. 저장소 생성
import uuid

from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from pydantic import BaseModel


class EmailState(BaseModel):
    title: str = ""
    email_detail: str = ""

# 2. 모델 호출
llm = ChatOllama(model = "gemma4:e4b", temperature=2)

# 3. 노드 / 라우터 함수 선언
def write_mail_node(state:EmailState) -> EmailState:
    """주어진 제목으로 이메일을 작성해주는 노드"""
    prompt = f"""
    당신은 사내메일 작성 담당자입니다.
    제목 - {state.title}
    에 대한 이메일을 정중하고 격식있는 어조로 한글로만 작성해주세요.
    불필요한 설명이나 참고, 팁 등은 필요없이 오직 이메일 내용만 적어주세요.
    """

    print("메일 작성중 ...")
    resp = llm.invoke(prompt)
    print(f"[메일 작성 완료]")
    content = resp.content.strip()
    print(content)
    state.email_detail = content
    return state

def send_mail_node(state:EmailState) -> None:
    """작성된 메일을 발송해주는 노드"""
    print("메일이 발송되었습니다.")
    print("[발송된 이메일 내용]")
    print(state.email_detail)


# 4.노드 등록
wf = StateGraph(EmailState)
wf.add_node("writer", write_mail_node)
wf.add_node("send", send_mail_node)

# 5. 엣지 조립
wf.set_entry_point("writer")
wf.add_edge("writer", "send")
wf.add_edge("send", END)

# 6. 컴파일 (저장소 및 정지포인트)
# checkpointer = 어디에 저장할 것인지
# interrupt_before = 어떤 노드 전에 멈출 것인지
memory = MemorySaver()
app = wf.compile(checkpointer=memory, interrupt_before=["send"])

# 7. 실행
# 현재 이것을 실행하는 thread id를 지정(어떤 프로세스인지 식별하기 위해서) 안한다면 아래와 같은 오류
# ValueError: Checkpointer requires one or more of the following 'configurable' keys: thread_id, checkpoint_ns, checkpoint_id
config = {"configurable" : {"thread_id" : uuid.uuid4()}}
result = app.invoke({"title" : "정리해고 및 인원감축으로 인해 권고사직 메일"}, config)

# 메모리에 뭐가 저장돼있는지 확인차원 (뭘 했는지? 다음에 어떤 노드가 대기중인지)
state_snapshot = app.get_state(config)
print(state_snapshot.values) # 현재 데이터 상태
print(state_snapshot.next) # 대기중인 노드

yn = input("작성된 초안을 승인하고 발송하시겠습니까?")
if yn.lower().strip() == "y":
    print("승인완료 발송 시작")
    print(f"memory = {memory}")
    app.invoke(None, config)
else:
    print("발송이 거부되었습니다.")
