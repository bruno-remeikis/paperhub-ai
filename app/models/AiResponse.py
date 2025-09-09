from typing import List, Optional

from dataclasses import dataclass

@dataclass
class Suggestion:
    change: str
    explanation: str

@dataclass
class AiResponse:
    suggestions: List[Suggestion]
    answer: str
    modifiedDocument: Optional[str]