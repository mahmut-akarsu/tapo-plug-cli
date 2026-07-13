from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("TAPO_EMAIL", "test@example.com")
    monkeypatch.setenv("TAPO_PASSWORD", "pass")
    monkeypatch.setenv(
        "TAPO_PLUGS",
        "priz2=192.168.1.220,priz3=192.168.1.144,priz4=192.168.1.252",
    )
    from api import app

    return TestClient(app)


@pytest.fixture
def mock_plug():
    plug = MagicMock()
    with patch("api.TapoPlug") as cls:
        cls.return_value = plug
        yield plug


def test_health(client):
    assert client.get("/health").json() == {"ok": True}


def test_list_plugs(client):
    data = client.get("/plugs").json()
    assert data["plugs"] == ["priz2", "priz3", "priz4"]


def test_on_by_id(client, mock_plug):
    r = client.post("/on/priz3")
    assert r.status_code == 200
    assert r.json() == {"ok": True, "action": "on", "plug_id": "priz3"}
    mock_plug.on.assert_called_once()


def test_off_by_id(client, mock_plug):
    r = client.post("/off/priz3")
    assert r.status_code == 200
    assert r.json() == {"ok": True, "action": "off", "plug_id": "priz3"}
    mock_plug.off.assert_called_once()


def test_unknown_plug(client):
    r = client.post("/off/priz99")
    assert r.status_code == 404
