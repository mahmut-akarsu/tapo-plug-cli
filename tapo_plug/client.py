from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, TypeVar

from tapo import ApiClient

from tapo_plug.config import TapoConfig, load_config_from_env
from tapo_plug.exceptions import TapoConfigError, TapoConnectionError

T = TypeVar("T")


class TapoPlug:
    """Tapo P100 priz kontrol sinifi.

    Ornekler:
        plug = TapoPlug(ip="192.168.1.50", email="a@b.com", password="sifre")
        plug.on()

        plug = TapoPlug.from_env()
        plug.off()
    """

    def __init__(
        self,
        config: TapoConfig | None = None,
        *,
        ip: str | None = None,
        email: str | None = None,
        password: str | None = None,
        preferred_protocol: str | None = None,
    ) -> None:
        if config is not None:
            self._config = config
        else:
            if not all([ip, email, password]):
                raise TapoConfigError(
                    "ip, email ve password verin veya TapoPlug.from_env() kullanin."
                )
            self._config = TapoConfig(
                ip=ip,
                email=email,
                password=password,
                preferred_protocol=preferred_protocol,
            )

        self._device = None

    @classmethod
    def from_env(cls, env_file: str | None = None) -> TapoPlug:
        return cls(config=load_config_from_env(env_file))

    @property
    def config(self) -> TapoConfig:
        return self._config

    @property
    def ip(self) -> str:
        return self._config.ip

    def on(self) -> None:
        async def _do() -> None:
            device = await self._get_device()
            await device.on()

        self._run(_do)

    def off(self) -> None:
        async def _do() -> None:
            device = await self._get_device()
            await device.off()

        self._run(_do)

    def toggle(self) -> None:
        async def _do() -> None:
            device = await self._get_device()
            info = await device.get_device_info()
            if info.device_on:
                await device.off()
            else:
                await device.on()

        self._run(_do)

    def get_info(self) -> dict[str, Any]:
        async def _do() -> dict[str, Any]:
            device = await self._get_device()
            info = await device.get_device_info()
            return {
                "device_on": info.device_on,
                "nickname": getattr(info, "nickname", None),
            }

        return self._run(_do)

    def get_name(self) -> str:
        info = self.get_info()
        return info.get("nickname") or "Tapo P100"

    def is_on(self) -> bool:
        return bool(self.get_info().get("device_on"))

    def status(self) -> dict[str, Any]:
        """Geriye uyumluluk icin get_info alias'i."""
        return self.get_info()

    async def _get_device(self):
        if self._device is None:
            client = ApiClient(self._config.email, self._config.password)
            self._device = await client.p100(self._config.ip)
        return self._device

    def _run(self, action: Callable[[], Awaitable[T]]) -> T:
        try:
            return asyncio.run(action())
        except Exception as exc:
            raise TapoConnectionError(
                f"Cihaz komutu basarisiz ({self._config.ip}): {exc}"
            ) from exc
