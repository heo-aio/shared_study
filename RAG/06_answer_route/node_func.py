from typing import TypedDict, List, Any

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph

from store_func import coll, load_excel_data
from utils import retrieve_to_text, python_code_parser, run_code


# State 객체
class State(TypedDict):
    question:str    # 질문
    generation:str  # 질문에 의해 생성된 답
    data:str        # 참고한 데이터
    code:str        # 요청 시 생성된 코드
    context:List[Any]   # 대화내용 저장

def get_state():
    return StateGraph(State)

# 최초 질문을 받아서 plain, excel, vector 중 하나를 받는다.
route_llm = ChatOllama(model="gemma4:e4b", format="json")

llm = ChatOllama(model="gemma4:e4b")

def init_answer(state:State):
    # print(f"state = {state}")
    q = state["question"]
    print(f"최초 질문 : {state["question"]}")
    sys_prompt = """
    당신은 사용자의 질문을 통해 RAG, 엑셀레이터 중 어느것을 활용할지 결정하는 전문가입니다.
    아래 내용을 참고하여 결정하세요.
    'excel' : 인공지능 데이터와 관련된 질문일 경우 선택
    'vector' : 인공지능 산업 동향 관련일 경우 선택
    'plain' : 위 두 경우 어디에도 속하지 않을 경우 선택
    
    [출력규칙]
    주어진 질문에 맞춰 "excel", "vector", "plain" 중 하나만 선택할 것
    다른 텍스트나 설명은 생성하지 말 것
    json 형태로 "route"라는 키에 대한 답으로 작성할 것
    예) {{"route" : "plain"}}
    """
    msg_list = []
    msg_list.append(("system", sys_prompt))
    msg_list.append(('human', "{question}"))
    route_prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = route_prompt|route_llm|JsonOutputParser()
    result = chain.invoke({"question":q})
    print(f"route result : {result}") # {'route': 'excel'} 식으로 출력

    return {"question" : q, "generation" : result["route"]}

def router(state:State):
    # print(f"router의 state = {state}")
    print("init_answer 내용을 통해 분기")
    # plain, excel, vector
    print(state["generation"])
    return state["generation"]

def plain_answer(state:State):
    print("학습한 내용 안에서 답변")
    q = state["question"]
    answer = llm.invoke(q)
    print(f"plain에서의 {answer}")
    return {"question" : q, "generation" : answer.content}

def excel_data(state:State):
    print("excel에서 데이터 참고 후 답변")
    q = state["question"]
    df = load_excel_data()
    sys_prompt = f"""
    당신은 주어진 데이터를 분석하는 데이터 분석가입니다.
    주어진 DataFrame으로 질문에 답할 수 있는 정보를 출력하는 파이썬 코드를 작성하세요.
    DataFrame이름은 excel_df이며, 다음과 같은 컬럼들이 있습니다.
    컬럼들 : {df.columns}
    데이터는 이미 로드되어 있으므로 데이터 로드 코드는 생략하세요.
    """

    msg_list = []
    msg_list.append(("system", sys_prompt))
    msg_list.append(('human', "{question}"))
    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt|llm|StrOutputParser()|python_code_parser
    code = chain.invoke({"question" : q})
    print(code)

    data = run_code("excel_df", df, code)

    return {"question" : q, "generation" : code,
            "code" : code, "data" : data}

def excel_answer(state:State):
    q = state["question"]
    context = state["data"]

    sys_prompt = f"""
    당신은 데이터를 바탕으로 질문에 답하는 데이터 분석가입니다.
    사용자가 입력한 질문을 제공된 데이털르 바탕으로 질문에 답하세요.
    """

    msg_list = []
    msg_list.append(("system", sys_prompt))
    msg_list.append(("human", "질문:{question}\n데이터:{context}"))

    prompt = ChatPromptTemplate.from_messages(msg_list)
    chain = prompt|llm|StrOutputParser()
    answer = chain.invoke({"question" : q, "context" : context})
    state["generation"] = answer

    return {"generation": answer}

def vector_db(state:State):
    print("RAG에서 데이터 참고 후 답변")
    q = state["question"]
    ret = coll.as_retriever(search_kwargs={"k":5}) # 컬렉션 검색 객체

    ret_chain = ret|retrieve_to_text
    data = ret_chain.invoke(q)
    print(f"참고자료 : {data}")

    msg_list = []
    msg_list.append(("system", "사용자의 질문을 제공하는 정보를 바탕으로 대답하세요."))
    msg_list.append(("human", "질문:{question}\n정보:{context}"))
    prompt = ChatPromptTemplate.from_messages(msg_list)

    chain = prompt|llm|StrOutputParser()
    answer = chain.invoke({"context" : data, "question" : q})

    return {"question" : q, "generation" : answer, "data" : data}
