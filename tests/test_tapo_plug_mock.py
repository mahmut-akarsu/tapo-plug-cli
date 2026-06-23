import json
from unittest.mock import patch

import pytest

from tapo_plug import TapoConfigError, TapoConnectionError, TapoPlug
from tapo_plug.config import TapoConfig, load_config_from_env
from tests.mock_credentials import MOCK_EMAIL, MOCK_IP, MOCK_PASSWORD


class TestTapoPlugMock:
    def test_on_acilir(self, mock_plug):
        plug, device = mock_plug

        plug.on()

        assert device.on_calls == 1
        assert device.device_on is True
        assert plug.is_on() is True

    def test_off_kapanir(self, mock_plug):
        plug, device = mock_plug
        device.device_on = True

        plug.off()

        assert device.off_calls == 1
        assert device.device_on is False
        assert plug.is_on() is False

    def test_toggle_durumu_degistirir(self, mock_plug):
        plug, device = mock_plug

        plug.toggle()
        assert device.on_calls == 1
        assert device.device_on is True

        plug.toggle()
        assert device.off_calls == 1
        assert device.device_on is False

    def test_ac_kapa_dongusu(self, mock_plug):
        plug, device = mock_plug

        assert plug.is_on() is False

        plug.on()
        assert device.on_calls == 1
        assert plug.is_on() is True

        plug.off()
        assert device.off_calls == 1
        assert plug.is_on() is False

    def test_get_info_ve_get_name(self, mock_plug):
        plug, device = mock_plug
        device.device_on = True

        info = plug.get_info()
        assert info["device_on"] is True
        assert plug.get_name() == "Mock P100"
        assert plug.ip == MOCK_IP

    def test_from_env_mock_dosyasi_ile_calisir(self, mock_from_env):
        plug, device = mock_from_env

        plug.on()
        assert device.device_on is True
        assert plug.config.email == MOCK_EMAIL

    def test_baglanti_hatasi_sarmalanir(self, mock_plug):
        plug, device = mock_plug

        async def failing_on() -> None:
            raise RuntimeError("network down")

        device.on = failing_on

        with pytest.raises(TapoConnectionError, match="network down"):
            plug.on()

    def test_eksik_parametreler_hata_verir(self):
        with pytest.raises(TapoConfigError):
            TapoPlug(ip=MOCK_IP, email=MOCK_EMAIL, password=None)

    def test_client_dogru_parametrelerle_olusturulur(self, mock_api_client):
        import asyncio

        plug = TapoPlug(ip=MOCK_IP, email=MOCK_EMAIL, password=MOCK_PASSWORD)
        asyncio.run(plug._get_device())

        client = mock_api_client[0]
        assert client.email == MOCK_EMAIL
        assert client.password == MOCK_PASSWORD


class TestTapoConfigMock:
    def test_load_config_from_env(self, mock_env_file):
        config = load_config_from_env(mock_env_file)

        assert config.ip == MOCK_IP
        assert config.email == MOCK_EMAIL
        assert config.password == MOCK_PASSWORD

    def test_eksik_env_degiskenleri(self, tmp_path, monkeypatch):
        monkeypatch.delenv("TAPO_IP", raising=False)
        monkeypatch.delenv("TAPO_EMAIL", raising=False)
        monkeypatch.delenv("TAPO_PASSWORD", raising=False)

        env_path = tmp_path / ".env"
        env_path.write_text("TAPO_IP=192.168.1.1\n", encoding="utf-8")

        with pytest.raises(TapoConfigError, match="TAPO_EMAIL"):
            load_config_from_env(env_path)

    def test_tapo_config_dogrulama(self):
        with pytest.raises(TapoConfigError, match="ip bos"):
            TapoConfig(ip="", email=MOCK_EMAIL, password=MOCK_PASSWORD)


class TestCliMock:
    def test_cli_on_mock(self, mock_from_env, capsys):
        with patch("cli.TapoPlug.from_env") as from_env_mock:
            plug, _device = mock_from_env
            from_env_mock.return_value = plug

            from cli import main

            with patch("sys.argv", ["cli.py", "on"]):
                exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Priz acildi." in captured.out

    def test_cli_ac_mock(self, mock_from_env, capsys):
        with patch("cli.TapoPlug.from_env") as from_env_mock:
            plug, _device = mock_from_env
            from_env_mock.return_value = plug

            from cli import main

            with patch("sys.argv", ["cli.py", "ac"]):
                exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Priz acildi." in captured.out

    def test_cli_off_mock(self, mock_from_env, capsys):
        with patch("cli.TapoPlug.from_env") as from_env_mock:
            plug, _device = mock_from_env
            from_env_mock.return_value = plug

            from cli import main

            with patch("sys.argv", ["cli.py", "off"]):
                exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Priz kapatildi." in captured.out

    def test_cli_kapat_mock(self, mock_from_env, capsys):
        with patch("cli.TapoPlug.from_env") as from_env_mock:
            plug, _device = mock_from_env
            from_env_mock.return_value = plug

            from cli import main

            with patch("sys.argv", ["cli.py", "kapat"]):
                exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Priz kapatildi." in captured.out

    def test_cli_status_mock(self, mock_from_env, capsys):
        with patch("cli.TapoPlug.from_env") as from_env_mock:
            plug, device = mock_from_env
            device.device_on = True
            from_env_mock.return_value = plug

            from cli import main

            with patch("sys.argv", ["cli.py", "status"]):
                exit_code = main()

        captured = capsys.readouterr()
        assert exit_code == 0
        payload = json.loads(captured.out)
        assert payload["device_on"] is True
