from __future__ import annotations

import json
from pathlib import Path

import click

from .app.services.index_builder import build_index
from .app.services.manifest import compute_manifest

DATA_PATH = Path("/data/in")
MANIFEST_FILE = Path("/data/manifest.json")


@click.group()
def cli() -> None:
    pass


@cli.command()
def build_index_cmd() -> None:
    old = json.loads(MANIFEST_FILE.read_text()) if MANIFEST_FILE.exists() else {}
    new = compute_manifest(DATA_PATH)
    build_index(old, new)
    MANIFEST_FILE.write_text(json.dumps(new, indent=2))


if __name__ == "__main__":
    cli()

