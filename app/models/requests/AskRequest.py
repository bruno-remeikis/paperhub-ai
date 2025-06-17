from pydantic import BaseModel


class AskRequest(BaseModel):
    document: str
    question: str