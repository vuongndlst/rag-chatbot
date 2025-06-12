from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .index_builder import build_index
from .manifest import compute_manifest

LOGGER = logging.getLogger(__name__)
DATA_PATH = Path("/data/in")
MANIFEST_FILE = Path("/data/manifest.json")


def load_manifest() -> dict[str, Any]:
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text())
    return {}


def save_manifest(manifest: dict[str, Any]) -> None:
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2))


class DebounceHandler(FileSystemEventHandler):
    def __init__(self, scheduler: BackgroundScheduler) -> None:
        self.scheduler = scheduler

    def on_any_event(self, event) -> None:  # noqa: ANN001
        self.scheduler.add_job(run_build_index, id="build", replace_existing=True, next_run_time=None, misfire_grace_time=10)


def run_build_index() -> None:
    old = load_manifest()
    new = compute_manifest(DATA_PATH)
    path = build_index(old, new)
    LOGGER.info("Index built at %s", path)
    save_manifest(new)


def start_watcher() -> Observer:
    scheduler = BackgroundScheduler()
    scheduler.start()
    handler = DebounceHandler(scheduler)
    observer = Observer()
    observer.schedule(handler, str(DATA_PATH), recursive=True)
    observer.start()
    return observer

