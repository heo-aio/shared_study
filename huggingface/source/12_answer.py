import torch
from anyio.streams.text import TextStream
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

model_id = "Qwen/Qwen2.5-1.5B-Instruct"

# 1. 토크나이저
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2. 모델
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype = torch.float16, # dtype = torch.bfloat16 <- 메모리 절약 및 안정성 확보(GPU에서 지원해야 사용가능)
    # attn_implementation = "flash_attention_2", # "eager", "sdpa"
    trust_remote_code=True,
    device_map = "auto"
)

prompt = input("AI에게 질문하고 싶은 내용은?\n")
print(prompt)

# 3. 토큰화
messages = [
    {"role": "system", "content": "넌 IT전문가이고, 유능한 신입을 키우기 위한 튜터야 알기 쉽게 설명을 잘해"},
    {"role": "user", "content": prompt}
]

text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
print(f"text = {text}")

inputs = tokenizer(text, return_tensors = "pt").to(model.device)

# 4. 추론
print("생각하는 중 ...")
# with torch.no_grad():
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens = 1024,
#         do_sample = True,
#         temperature = 0.7,
#         eos_token_id = tokenizer.eos_token_id
#     )
#     print(tokenizer.decode(outputs[0]))

# 실시간 출력을 위해서는 Streamer가 필요하다
streamer = TextStreamer(tokenizer, skip_prompt=True)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens = 1024,
        do_sample = True,
        temperature = 0.7,
        eos_token_id = tokenizer.eos_token_id,
        streamer = streamer
    )