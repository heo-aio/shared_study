import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen2.5-1.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)

text = "SDPA와 EAGER 중에 누가 더 빠를까 비교해보기" * 30
inputs = tokenizer(text, return_tensors="pt").to("cuda")
print(f"입력 토큰 수 : {inputs['input_ids'].shape[1]}개")

def benchmark(attn_type, name):
    print(f"=== [{name}] 측정시작 ===")
    # 모델 불러오기
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        dtype = torch.float16,
        low_cpu_mem_usage = True, # CPU, Memory 절약
        attn_implementation = attn_type,
        device_map="auto"
    )

    # 실행
    start_time = time.time()
    with torch.no_grad():
        model(inputs["input_ids"])

    # CPU가 GPU작업 종료까지 기다리도록 동기화 시켜준다.
    torch.cuda.synchronize()
    end_time = time.time() - start_time
    print(f"=== [{name}]이 걸린시간 : {end_time} ===")

# benchmark("sdpa", "FlashAttention 방식(SDPA)") # 6.340752601623535
benchmark("eager", "Standard Attention 방식(EAGER)") # 6.212922811508179