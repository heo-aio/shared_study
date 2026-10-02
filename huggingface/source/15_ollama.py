# uv pip install ollama
from ollama import chat, Client

text = input("ollama와 대화해보기 \n")
# host 설정을 0.0.0.0으로 했을 경우
# client = Client(host = "http://192.168.1.40:11434")

def chat_generate(text):
    print(f"입력 내용 : {text}")
    print(f"생각중 ...")
    resp = chat(
        model = "exaone3.5:2.4b",
        messages = [{"role" : "user", "content" : text}]
    )

    print(f"답변 : {resp.message.content}")

def chat_stream(input):
    # ollama rm [삭제할 모델 이름]
    print(f"입력 내용 : {input}")
    print(f"생각중 ...")
    resp = chat(
        model = "hf.co/Jackrong/Qwen3.5-4B-Claude-4.6-Opus-Reasoning-Distilled-GGUF:latest",
        messages = [{"role" : "user", "content" : input}],
        stream = True
    )

    for chunk in resp:
        # end = ""가 없으면 한글자라 찍힐 때 마다 줄바꿈이 된다.
        # flush = True는 stream에 남아있는 잔여 데이터를 모두 밖으로 내보낸다.
        print(chunk.message.content, end = "", flush = True)

# chat_generate(text)

chat_stream(text)