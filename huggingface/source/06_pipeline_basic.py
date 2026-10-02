# window 경고메시지 지우기 (선택사항)
import os

from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINK_WARING"] = "1"

"""
clf = pipeline(task = "text-classification")
print(f"model_name : {clf.model.name_or_path}")
print(clf("Hugging Face is Amazing~!~!~"))
print(clf("짜증나"))
"""

# 질의응답
# 모델명을 넣었더니 해당 task가 pipeline에 없다고 한다.
# transformers의 버전을 낮춰주면 가능
# pip install transformers==4.57.6
"""
qna = pipeline(model = "monologg/koelectra-base-v3-finetuned-korquad")

result = qna(
    question = "대한민국의 수도는 어디입니까?",
    context = "대한민국의 수도는 서울입니다.",
)
print(result)
"""


# 이미지 분류
# uv pip install pillow torchvision
vision = pipeline(model = "google/vit-base-patch16-224")
print(vision('dog.png'))