from pydantic import BaseModel

Emotion = ["기쁨", "슬픔", "평온", "불안", "지침"]

class DiaryEntry(BaseModel):
    text: str

class AnalyzeResult(BaseModel):
    emotion: str
    comment: str