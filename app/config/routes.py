from fastapi import APIRouter

from app.models.requests.AskRequest import AskRequest
import app.ai_service as ai

ai_router = APIRouter(
    tags=["ai"],
    responses={404: {"description": "Not found"}},
)

@ai_router.post("/ask")
async def ask_question(req: AskRequest):
    res = ai.ask(req)
    return res