from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import traceback

import ai_service as ai

from pydantic import BaseModel


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
    return {
        'status': 'error',
        'error': str(e)
    }


@app.get('/')
async def index():
    return { "message": "API is running..." }


class Document(BaseModel):
    content: str


@app.post('/refs')
async def refs(doc: Document):
    #return doc.content
    return ai.ask(doc.content)