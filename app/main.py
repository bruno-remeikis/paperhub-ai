from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import traceback

from models.requests.AskRequest import AskRequest
import ai_service as ai


# Inicia API
app = FastAPI()

# Adiciona middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def buildErrorResponse(e: Exception):
    traceback.print_exc()
    return {"status": "error", "error": str(e)}


@app.get("/")
async def index():
    return {"message": "API is running..."}


@app.post("/ask")
async def ask(req: AskRequest):
    res = ai.ask(req)
    return res
