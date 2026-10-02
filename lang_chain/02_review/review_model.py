from pydantic import BaseModel, Field

# 주로 대형 언어 모델(LLM)과 연동하여 AI로부터 일정한 형식의 구조화된 데이터(Structured Output)를
# 안전하게 받아내고 싶을 때 사용
class ReviewAnalysis(BaseModel):
    # description은 사람이 보라고 적어둔 주석이 아니라 AI에게 주는 가이드라인
    sentiment: str = Field(description="긍정, 부정, 중립 중 하나")
    score: int = Field(description="1점부터 5점까지 만족도 점수, 절대 1보다 작지않고, 5보다 크지 않은 정수여야 함")
    summary: str = Field(description="리뷰 핵심 내용을 한 줄 요약")



# Pydantic 모델을 정의해 두면, OpenAI나 프레임워크(FastAPI, LangChain 등)에서 LLM을 호출할 때
# 이 스키마를 전달하여 AI가 마음대로 텍스트를 뱉는 것이 아니라,
# 정확히 정의된 타입과 조건에 맞는 JSON 데이터를 반환하도록 강제할 수있음