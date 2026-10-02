import contextlib
import io


def retrieve_to_text(docs):
    text = ""
    for doc in docs:
        text += doc.page_content+"\n"

    return text

# 대답에서 코드만 추출
def python_code_parser(text:str):
    # 대답 중에서 ```python으로 감싸진 부분만 받아오는 함수
    # ```python -> ``` -> [```, code내용, ```]
    code_list = text.replace("```python", "```").strip().split("```")

    # ```이 없이 답이 나왔을 때, 앞선 코드에서 끊지 못한 경우 코드를 그대로 내보낸다.
    if len(code_list) == 1:
        return code_list[0]

    return code_list[1]

# 추출한 코드 실행
def run_code(df_name, df, input_code:str):
    # 코드를 실행했을 때, print된 내용을 보고싶다.
    output = io.StringIO() # 문자열이 오고갈 수 있는 객체

    try:
        # 무언가 출력이 나오면 output으로 보내서 저장해라
        # 아래 코드가 실행되는 동안만(with로 인해 다 끝나면 자동으로 자원은 닫힌다.)
        with contextlib.redirect_stdout(output):
            # exec(code, 필요한 변수)
            exec(input_code, {df_name:df})
            # result = df_inkjet[df_inkjet['Velocity'] == max_velocity]
    except Exception as e:
        print(f"Error: {e}", file=output)

    return output.getvalue()