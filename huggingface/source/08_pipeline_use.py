import os

from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNINGS"] = "1"

model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

# pip install accelerate
pipe = pipeline(task = "text-generation", model = model_id, device_map = "auto")

q = input("아무거나 모든지 질문 ㄱㄱ\n")

result = pipe(
    q,
    max_new_tokens = 1024,
    do_sample = True,
    temperature = 0.7,
    top_p = 0.9
)

print(result[0]['generated_text'])