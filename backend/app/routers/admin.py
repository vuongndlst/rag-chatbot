from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..deps import get_retriever

router = APIRouter(prefix="/admin")


@router.post("/reload")
async def reload_index(retriever=Depends(get_retriever)):
    """Reload the current index."""
    try:
        retriever._persist_directory  # Access to trigger load
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc))
    return {"status": "reloaded"}

