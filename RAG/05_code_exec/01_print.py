import contextlib
import io

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
import pandas as pd

# 1. 모델 설정 및 지정
llm = ChatOllama(model="gemma4:e4b")

# 2. 데이터 불러오기
data_path = "data/InkjetDB_preprocessing.csv"
df_inkjet = pd.read_csv(data_path, index_col=0)
columns = ",".join(df_inkjet.columns)
# print(columns)

# 3. 데이터 분석 프롬프트 작성
system_prompt = f"""
    당신은 주어진 데이터를 분석하는 데이터 분석가입니다.
    주어진 DataFrame으로 질문에 답할 수 있는 정보를 출력하는 파이썬 코드를 작성하세요.
    DataFrame이름은 df_inkjet이며, 다음과 같은 컬럼들이 있습니다.
    컬럼들 : {columns}
    데이터는 이미 로드되어 있으므로 데이터 로드 코드는 생략하세요.
"""

print(system_prompt)

# 4. 프롬프트 조립 후 실행
# 'human', 'user', 'ai', 'assistant', 'system'
msg_list = [ # 메시지 리스트 안에 개별 메시지는 Tuple 형태여야 한다.
    ("system", system_prompt),  # AIMessage(content=system_prompt)
    ("human", "{question}")     # HumanMessage(content="{question}")
]
prompt = ChatPromptTemplate.from_messages(msg_list)

code_gen_chain = {"question" : RunnablePassthrough()}|prompt|llm|StrOutputParser()
# result = code_gen_chain.invoke("Velocity가 가장 큰 데이터를 찾고 싶어")
# print(result)

# 5. 대답에서 코드만 추출
def python_code_parser(text:str):
    # 대답 중에서 ```python으로 감싸진 부분만 받아오는 함수
    # ```python -> ``` -> [```, code내용, ```]
    code_list = text.replace("```python", "```").strip().split("```")

    # ```이 없이 답이 나왔을 때, 앞선 코드에서 끊지 못한 경우 코드를 그대로 내보낸다.
    if len(code_list) == 1:
        return code_list[0]

    return code_list[1]

# print("###"*30)
# print(python_code_parser(result))
# print("###"*30)

# 6. chain으로 코드 추출 조합 -> 출력된 내용을 output에 담아 밖으로 내보냄
code_extract_chain = code_gen_chain|python_code_parser
print(code_extract_chain.invoke("Velocity가 가장 큰 데이터를 찾고 싶어"))

# 7. 추출한 코드 실행
def run_code(input_code:str):
    # 코드를 실행했을 때, print된 내용을 보고싶다.
    output = io.StringIO() # 문자열이 오고갈 수 있는 객체

    try:
        # 무언가 출력이 나오면 output으로 보내서 저장해라
        # 아래 코드가 실행되는 동안만(with로 인해 다 끝나면 자동으로 자원은 닫힌다.)
        with contextlib.redirect_stdout(output):
            # exec(code, 필요한 변수)
            exec(input_code, {"df_inkjet":df_inkjet})
            # result = df_inkjet[df_inkjet['Velocity'] == max_velocity]
    except Exception as e:
        print(f"Error: {e}", file=output)

    return output.getvalue()

# 코드 실행 결과 보기
code_exec_chain = code_extract_chain | run_code
print(code_exec_chain.invoke("Velocity가 가장 큰 데이터를 찾아줘"))