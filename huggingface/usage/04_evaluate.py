# uv pip install evaluate scikit-learn
import evaluate

# 1. 평가지표 로딩
acc = evaluate.load('accuracy')

# 2. 예측값과 정답을 주고 결과 계산
result = acc.compute(
    predictions = [1, 0, 1, 1], # 예측
    references = [1, 1, 0, 1] # 정답
)

print(result)