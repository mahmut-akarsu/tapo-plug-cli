#!/usr/bin/env python3
import argparse
import json
import sys

from tapo_plug import TapoConfigError, TapoConnectionError, TapoPlug

COMMANDS = {
    "on": "on",
    "ac": "on",
    "off": "off",
    "kapat": "off",
    "toggle": "toggle",
    "status": "status",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tapo P100 priz kontrolu",
        epilog="Ornek: python cli.py ac   |   python cli.py kapat",
    )
    parser.add_argument(
        "command",
        choices=sorted(COMMANDS.keys()),
        help="on/ac=ac, off/kapat=kapat, toggle=degistir, status=durum",
    )
    args = parser.parse_args()
    action = COMMANDS[args.command]

    try:
        plug = TapoPlug.from_env()
    except TapoConfigError as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 1

    try:
        if action == "on":
            plug.on()
            print("Priz acildi.")
        elif action == "off":
            plug.off()
            print("Priz kapatildi.")
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
