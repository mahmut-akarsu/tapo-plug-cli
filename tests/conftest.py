from __future__ import annotations

import pytest

from tests.mock_credentials import (
    MOCK_DEVICE_NAME,
    MOCK_EMAIL,
    MOCK_IP,
    MOCK_PASSWORD,
)


class MockDeviceInfo:
    def __init__(self, device_on: bool = False, nickname: str = MOCK_DEVICE_NAME) -> None:
        self.device_on = device_on
        self.nickname = nickname


class MockTapoDevice:
    def __init__(self, ip: str) -> None:
        self.ip = ip
        self.device_on = False
        self.on_calls = 0
        self.off_calls = 0

    async def on(self) -> None:
        self.on_calls += 1
        self.device_on = True

    async def off(self) -> None:
        self.off_calls += 1
        self.device_on = False

    async def get_device_info(self) -> MockDeviceInfo:
        return MockDeviceInfo(device_on=self.device_on)


class MockApiClient:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self.devices: dict[str, MockTapoDevice] = {}

    async def p100(self, ip: str) -> MockTapoDevice:
        if ip not in self.devices:
            self.devices[ip] = MockTapoDevice(ip)
        return self.devices[ip]


@pytest.fixture
def mock_api_client(monkeypatch):
    created: list[MockApiClient] = []

    def factory(email: str, password: str) -> MockApiClient:
        client = MockApiClient(email, password)
        created.append(client)
        return client

    monkeypatch.setattr("tapo_plug.client.ApiClient", factory)
    return created


@pytest.fixture
def mock_plug(mock_api_client):
    import asyncio

    from tapo_plug import TapoPlug

    plug = TapoPlug(ip=MOCK_IP, email=MOCK_EMAIL, password=MOCK_PASSWORD)
    asyncio.run(plug._get_device())
    device = mock_api_client[0].devices[MOCK_IP]
    return plug, device


@pytest.fixture
def mock_env_file(tmp_path, monkeypatch):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                f"TAPO_IP={MOCK_IP}",
                f"TAPO_EMAIL={MOCK_EMAIL}",
                f"TAPO_PASSWORD={MOCK_PASSWORD}",
            ]
        ),
        encoding="utf-8",
    )
    return env_path


@pytest.fixture
def mock_from_env(mock_api_client, mock_env_file):
    import asyncio

    from tapo_plug import TapoPlug

    plug = TapoPlug.from_env(str(mock_env_file))
    asyncio.run(plug._get_device())
    device = mock_api_client[0].devices[MOCK_IP]
    return plug, device
