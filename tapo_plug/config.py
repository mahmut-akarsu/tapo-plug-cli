from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from tapo_plug.exceptions import TapoConfigError


@dataclass(frozen=True)
class TapoConfig:
    ip: str
    email: str
    password: str
    preferred_protocol: str | None = None

    def __post_init__(self) -> None:
        if not self.ip.strip():
            raise TapoConfigError("ip bos olamaz.")
        if not self.email.strip():
            raise TapoConfigError("email bos olamaz.")
        if not self.password:
            raise TapoConfigError("password bos olamaz.")


def _env_path(env_file: Path | str | None) -> Path:
    if env_file is None:
        return Path(__file__).resolve().parent.parent / ".env"
    return Path(env_file)


def _credentials() -> tuple[str, str, str | None]:
    email = os.getenv("TAPO_EMAIL", "").strip()
    password = os.getenv("TAPO_PASSWORD", "").strip()
    preferred_protocol = os.getenv("TAPO_PROTOCOL", "").strip() or None

    missing = [
        name
        for name, value in [("TAPO_EMAIL", email), ("TAPO_PASSWORD", password)]
        if not value
    ]
    if missing:
        raise TapoConfigError(
            f"Eksik ortam degiskeni: {', '.join(missing)}. "
            f".env dosyasini kontrol edin."
        )

    return email, password, preferred_protocol


def load_plugs_from_env(env_file: Path | str | None = None) -> dict[str, TapoConfig]:
    load_dotenv(_env_path(env_file))
    email, password, preferred_protocol = _credentials()

    plugs_raw = os.getenv("TAPO_PLUGS", "").strip()
    if plugs_raw:
        plugs: dict[str, TapoConfig] = {}
        for part in plugs_raw.split(","):
            part = part.strip()
            if not part:
                continue
            if "=" not in part:
                raise TapoConfigError(f"Gecersiz priz tanimi: {part}")
            plug_id, ip = part.split("=", 1)
            plug_id = plug_id.strip()
            ip = ip.strip()
            if not plug_id or not ip:
                raise TapoConfigError(f"Gecersiz priz tanimi: {part}")
            plugs[plug_id] = TapoConfig(
                ip=ip,
                email=email,
                password=password,
                preferred_protocol=preferred_protocol,
            )
        if not plugs:
            raise TapoConfigError("TAPO_PLUGS bos.")
        return plugs

    ip = os.getenv("TAPO_IP", "").strip()
    if not ip:
        raise TapoConfigError("TAPO_PLUGS veya TAPO_IP tanimli olmali.")

    return {
        "default": TapoConfig(
            ip=ip,
            email=email,
            password=password,
            preferred_protocol=preferred_protocol,
        )
    }


def get_plug_config(plug_id: str, env_file: Path | str | None = None) -> TapoConfig:
    plugs = load_plugs_from_env(env_file)
    if plug_id not in plugs:
        known = ", ".join(sorted(plugs))
        raise TapoConfigError(f"Priz bulunamadi: {plug_id}. Mevcut: {known}")
    return plugs[plug_id]


def load_config_from_env(env_file: Path | str | None = None) -> TapoConfig:
    plugs = load_plugs_from_env(env_file)
    if len(plugs) == 1:
        return next(iter(plugs.values()))
    if "default" in plugs:
        return plugs["default"]
    return next(iter(plugs.values()))
