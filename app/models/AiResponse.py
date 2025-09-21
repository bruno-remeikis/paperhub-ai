from typing import List, Optional
from pydantic import BaseModel


class Suggestion(BaseModel):
    change: str
    explanation: str


class AiResponse(BaseModel):
    suggestions: List[Suggestion]
    answer: str
    modifiedDocument: Optional[str]