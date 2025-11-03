from dotenv import load_dotenv
from fastapi import FastAPI

from app.config import routes

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

ALLOWED_ORIGINS = ["http://localhost:3100", "https://localhost:3000", "https://paperhub.com.br"]

def create_app():
    app = FastAPI()
    app.include_router(routes.ai_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

application = create_app()
