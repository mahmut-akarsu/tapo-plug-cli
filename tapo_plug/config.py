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


def load_config_from_env(env_file: Path | str | None = None) -> TapoConfig:
    if env_file is None:
        env_path = Path(__file__).resolve().parent.parent / ".env"
    else:
        env_path = Path(env_file)

    load_dotenv(env_path)

    ip = os.getenv("TAPO_IP", "").strip()
    email = os.getenv("TAPO_EMAIL", "").strip()
    password = os.getenv("TAPO_PASSWORD", "").strip()
    preferred_protocol = os.getenv("TAPO_PROTOCOL", "").strip() or None

    missing = [
        name
        for name, value in [("TAPO_IP", ip), ("TAPO_EMAIL", email), ("TAPO_PASSWORD", password)]
        if not value
    ]
    if missing:
        raise TapoConfigError(
            f"Eksik ortam degiskeni: {', '.join(missing)}. "
            f".env.example dosyasini .env olarak kopyalayip doldurun."
        )

    return TapoConfig(
        ip=ip,
        email=email,
        password=password,
        preferred_protocol=preferred_protocol,
    )
