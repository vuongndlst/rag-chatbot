from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveTextSplitter
from langchain_chroma import Chroma


INDEX_BASE = Path("/data/index")
DATA_PATH = Path("/data/in")


def build_index(manifest_old: dict[str, Any], manifest_new: dict[str, Any]) -> Path:
    """Build or update index and promote atomically."""
    if not diff_needed(manifest_old, manifest_new):
        return INDEX_BASE / "current"

    tmp_dir = Path(f"/tmp/index_build_{uuid.uuid4().hex}")
    collection = Chroma(
        collection_name="docs",
        embedding_function=OpenAIEmbeddings(),
        persist_directory=str(tmp_dir),
    )

    splitter = RecursiveTextSplitter()
    for file_str, meta in manifest_new.items():
        file = Path(file_str)
        if file_str not in manifest_old or manifest_old[file_str]["sha256"] != meta["sha256"]:
            text = file.read_text(errors="ignore")
            docs = splitter.create_documents([text], metadatas=[{"source": file_str}])
            collection.add_documents(docs)

    collection.persist()

    target_version = INDEX_BASE / f"v{uuid.uuid4().hex}"
    os.rename(tmp_dir, target_version)
    current_symlink = INDEX_BASE / "current"
    if current_symlink.is_symlink() or current_symlink.exists():
        current_symlink.unlink()
    current_symlink.symlink_to(target_version)
    return target_version


def diff_needed(old: dict[str, Any], new: dict[str, Any]) -> bool:
    return json.dumps(old, sort_keys=True) != json.dumps(new, sort_keys=True)

