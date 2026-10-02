import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "google/gemma-2-2b-it"
# 토크나이저 생성
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 대화 내용을 정의
msg_list = [
    {"role" : "user", "content" : "파이썬에서 변수가 뭐야?"},
    {"role" : "assistant", "content" : "변수를 데이터를 저장하는 상자와 같아"},
    {"role" : "user", "content" : "그럼 리스트는 뭐야?"}
]

prompt = tokenizer.apply_chat_template(
    msg_list,
    tokenize = False, # False : 토큰화 된 내용을 문자열로 반환
    add_generation_prompt = True, # True : msg_list이후 assistant가 이어쓸 수 있을지 여부
)

# print(f"모델에 입력될 최종 텍스트 포맷 : {prompt}")

# 문자열화된 토큰을 숫자(ids)로 변환
inputs = tokenizer(prompt, return_tensors = "pt").to("cuda")
print(f"{prompt} \n\n {inputs}")

# 모델 호출
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype = torch.float32,
    device_map = "auto" # GPU랑 CPU가 있으면 알아서 할당해주는 파라미터
)

# 답변 생성
# 토큰화된 입력(숫자들)을 바탕으로, 모델이 다음에 올 글자들을 차례차례 이어서 최종 텍스트(답변)를 생성해 내는 함수
# pip install accelerate
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens = 256, # 생성할 최대 토큰 수
        temperature = 0.7, # 창의성 (0 : 있는 그대로 ~ 1 : 창의적)
        do_sample = True # 창의성 관련
    )

# print(outputs[0])
resp_text = tokenizer.decode(outputs[0], skip_special_tokens = True)
# 현재 resp_text는 질문내용 + 답변 형태
# 답변만 받고 싶다면 ? outputs[0][입력내용제외한 나머지]형태로 해야한다.
print(resp_text)