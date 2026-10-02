import os

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModel

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNINGS"] = "1"

model_id = "klue/bert-base" # task = fill-mask

# 1. 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2. 모델 불러오기
model = AutoModel.from_pretrained(model_id)

# 3. 토큰화
text = "파이썬이라는 언어는 참 재미있습니다."
inputs = tokenizer(text, return_tensors="pt")
print(f"Token화된 tensor = {inputs}")

# 4. 모델 추론
with torch.no_grad():
    # output_hidden_states = True로하면 모든 레이어의 hidden state를 받는다.
    outputs = model(**inputs, output_hidden_states = False)

# last_hidden_state
print(f"outputs = {outputs}")

lhs = outputs.last_hidden_state
print(f"last_hidden_states shape = {lhs.shape}") # [1, 13, 768]

# 1 : 문장 1개
# 13 : special token을 포함한 토큰의 수
# 768 : BERT모델의 표현 차원

# 5. 활용 예시 - 특정 단어의 벡터 가져오기
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
print(f"결과 = {tokens}")

# 토큰 별로 768차원 벡터를 가져와보기 (앞 3차원만 ...)
for idx, token in enumerate(tokens):
    # lhs[0][idx][:3] == lhs[0, idx, :3]
    vect = lhs[0, idx, :3].tolist()
    print(f"{idx} : {token} -> vector : {vect}...")

    # 768개의 배열에는 무엇이 있을까
    # 단어를 구분할 수 있는 기준 조건 (Feature)
    # 단일 단어 뿐 아니라 인근의 단어들과의 관계도 포함이 된다.

# last_hidden_state는 문장안의 모든 각 단어의 의미를 담은 벡터를 확인할 때