from fastapi import FastAPI

from app.config import routes


def create_app():
    app = FastAPI()
    app.include_router(routes.ai_router)
    return app

application = create_app()
