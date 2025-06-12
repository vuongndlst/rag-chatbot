from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.app.main import create_app


def test_chat_endpoint():
    app = create_app()
    client = TestClient(app)
    response = client.post("/chat", json={"query": "hello"})
    assert response.status_code == 200
