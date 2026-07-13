#!/usr/bin/env python3
import argparse
import json
import sys

from tapo_plug import TapoConfigError, TapoConnectionError, TapoPlug, get_plug_config

COMMANDS = {
    "on": "on",
    "ac": "on",
    "off": "off",
    "kapat": "off",
    "toggle": "toggle",
    "status": "status",
}


def _resolve_plug(plug_id: str | None) -> TapoPlug:
    if plug_id:
        return TapoPlug(config=get_plug_config(plug_id))
    return TapoPlug.from_env()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tapo P100 priz kontrolu",
        epilog="Ornek: python cli.py off priz4   |   python cli.py ac",
    )
    parser.add_argument(
        "command",
        choices=sorted(COMMANDS.keys()),
        help="on/ac=ac, off/kapat=kapat, toggle=degistir, status=durum",
    )
    parser.add_argument(
        "plug_id",
        nargs="?",
        default=None,
        help="Opsiyonel priz id (orn: priz4 veya 4 → priz4)",
    )
    args = parser.parse_args()
    action = COMMANDS[args.command]

    plug_id = args.plug_id
    if plug_id and plug_id.isdigit():
        plug_id = f"priz{plug_id}"

    try:
        plug = _resolve_plug(plug_id)
    except TapoConfigError as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 1

    try:
        if action == "on":
            plug.on()
            label = plug_id or "default"
            print(f"Priz acildi ({label}).")
        elif action == "off":
            plug.off()
            label = plug_id or "default"
            print(f"Priz kapatildi ({label}).")
        elif action == "toggle":
            plug.toggle()
            print("Priz durumu degistirildi.")
        else:
            info = plug.get_info()
            print(json.dumps(info, indent=2, ensure_ascii=False))
    except TapoConnectionError as exc:
        print(f"Baglanti hatasi: {exc}", file=sys.stderr)
        print(
            "Kontrol: ayni Wi-Fi, dogru IP, Tapo uygulamasinda "
            "Ucuncu Taraf Uyumlulugu acik mi?",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
