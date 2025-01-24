from fastapi import FastAPI
from app.api.routes import user_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_router)
    return app