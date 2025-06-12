from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def compute_manifest(path: Path) -> dict[str, Any]:
    """Compute manifest mapping file to sha256 and mtime."""
    manifest: dict[str, Any] = {}
    for file in path.glob("**/*"):
        if file.is_file() and file.suffix in {".pdf", ".docx"}:
            sha = hashlib.sha256(file.read_bytes()).hexdigest()
            manifest[str(file)] = {"sha256": sha, "mtime": file.stat().st_mtime}
    return manifest


def diff(old: dict[str, Any], new: dict[str, Any]) -> bool:
    """Return True if manifests differ."""
    return json.dumps(old, sort_keys=True) != json.dumps(new, sort_keys=True)

