# 1. 로컬에서 학습을 마친 모델과 토크나이저 로드
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_id = 'distilbert-base-uncased'
model_path = "./fine_tuned_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# 2. hugging face에 Push
# 토큰의 권한이 write여야 가능
repo_id = "HeoJungMo/model_upload_test"
print("model과 토크나이저 업로드 ing ...")
tokenizer.push_to_hub(repo_id)
model.push_to_hub(repo_id)
print("업로드 성공")
