from __future__ import annotations

from pathlib import Path

import os

from fastapi import Depends
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain_chroma import Chroma

INDEX_PATH = Path("/data/index/current")


def get_retriever() -> Chroma:
    """Return Chroma retriever from current index."""
    return Chroma(persist_directory=str(INDEX_PATH))


def get_llm() -> OpenAI:
    """Return OpenAI LLM configured for streaming."""
    api_key = os.environ.get("OPENAI_API_KEY", "test")
    return OpenAI(streaming=True, openai_api_key=api_key)

