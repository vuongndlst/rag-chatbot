from fastapi import FastAPI

from .routers import chat, admin


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(title="RAG Chatbot")
    app.include_router(chat.router)
    app.include_router(admin.router)
    return app

