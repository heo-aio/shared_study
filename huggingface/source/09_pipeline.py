import os

from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNINGS"] = "1"

clf = pipeline(task = "text-classification", device = 0)
result = clf(
    "오늘 파이프라인과 오토 모델을 배웠는데 재미있었다는 뻥이고 이걸 내가 응용하고 활용할 수 있을까라는 걱정이 들었다"
)
print(result)