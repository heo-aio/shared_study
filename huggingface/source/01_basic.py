# uv pip install transformers

# import library
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

# load model
model_id = "Copycats/koelectra-base-v3-generalized-sentiment-analysis"

# 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 모델(사전 학습된) 불러오기
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# 모델과 토크나이저를 주고, 일을 수행시킬 도구를 만든다.
# 본래는 세부적인 작업이 필요하지만, Pipeline으로 간소화 함
sentiment_classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model)

# target reviews
review_list = [
    '이쁘고 좋아요~~~씻기도 편하고 아이고 이쁘다고 자기방에 갖다놓고 잘써요~^^',
    '아직 입어보진 않았지만 굉장히 가벼워요~~ 다른 리뷰처럼 어깡이 좀 되네요ㅋ 만족합니다. 엄청 빠른발송 감사드려요 :)',
    '재구매 한건데 너무너무 가성비인거 같아요!! 다음에 또 생각나면 3개째 또 살듯..ㅎㅎ',
    '가습량이 너무 적어요. 방이 작지 않다면 무조건 큰걸로구매하세요. 물량도 조금밖에 안들어가서 쓰기도 불편함',
    '한번입었는데 옆에 봉제선 다 풀리고 실밥도 계속 나옵니다. 마감 처리 너무 엉망 아닌가요?',
    '따뜻하고 좋긴한데 배송이 느려요',
    '맛은 있는데 가격이 있는 편이에요',
    '맛이 존나 없어요',
    '누가 추천해줬는지 원망스러워요',
    '핏이 딱 떨어져서 이뻐요'
]

# predict
for review in review_list:
  pred = sentiment_classifier(review)
  print(f"pred : {pred}")
  print(f'{review}\n>> {pred[0]}')

"""
Hugging Face 로그인 방법
hf auth login <- 로그인 방법
hf auth logout <- 로그아웃
hf auth whoami <- 현재 로그인 계정
hf download [model] --local-dir [경로] <- 모델 다운로드 (경로까지 지정가능)

토큰과 브라우저 중 택1 하라고 함
토큰 선택 시 복사한 토큰을 넣으면 됨 (토큰은 보이지 않음)
"""
