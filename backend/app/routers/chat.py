from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..deps import get_retriever, get_llm

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


def stream_response(generator):
    for chunk in generator:
        yield f"data: {chunk}\n\n"


@router.post("/chat")
async def chat(req: ChatRequest, retriever=Depends(get_retriever), llm=Depends(get_llm)):
    """Retrieve relevant docs via hybrid search and stream answer."""
    # Simple echo for testing
    def gen():
        yield f"You asked: {req.query}"
    return StreamingResponse(stream_response(gen()), media_type="text/event-stream")

