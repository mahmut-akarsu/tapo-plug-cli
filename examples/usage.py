"""Baska bir Python projesinden TapoPlug sinifi kullanimi."""

from tapo_plug import TapoConfig, TapoPlug


def with_explicit_credentials() -> None:
    plug = TapoPlug(
        ip="192.168.1.50",
        email="email@gmail.com",
        password="sifre",
    )
    plug.on()
    print(f"Priz acik mi: {plug.is_on()}")
    plug.off()


def with_config_object() -> None:
    config = TapoConfig(
        ip="192.168.1.50",
        email="email@gmail.com",
        password="sifre",
    )
    plug = TapoPlug(config=config)
    plug.toggle()


def from_env_file() -> None:
    plug = TapoPlug.from_env()
    info = plug.get_info()
    print(plug.get_name(), info)


if __name__ == "__main__":
    from_env_file()
