# 1. 평가지표들 불러오기
import evaluate

print("평가 지표 로드 ...")

metrics = evaluate.combine([
    evaluate.load("accuracy"),  # 정확도
    evaluate.load("f1"),        # 일치도
    evaluate.load("precision"), # 정밀도
    evaluate.load("recall")     # 재현율
])

# 2. 예측값과 정답 넣기
result = metrics.compute(
    predictions = [0, 1, 1, 0, 1],
    references = [0, 1, 1, 0, 0]
)

# 3. 결과 출력
print(result)
# {'accuracy': 0.8, 'f1': 0.8, 'precision': 0.6666666666666666, 'recall': 1.0}
