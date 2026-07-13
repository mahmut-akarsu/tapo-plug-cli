# tapo-plug

Tapo P100 priz kontrolu — CLI ve Python sinifi.

## Kurulum

```powershell
git clone https://github.com/mahmut-akarsu/tapo-plug-cli.git
cd tapo-plug-cli
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
```

`.env` dosyasina priz IP, Tapo e-posta ve sifrenizi yazin.

## API (Tailscale / uzak erisim)

Prizle ayni agdaki PC'de cift tikla:

```
baslat-api.bat
```

Veya manuel:

```powershell
.\.venv\Scripts\uvicorn api:app --host 0.0.0.0 --port 8000
```

Uzak PC'den (orn. `100.116.215.46`):

```powershell
curl -X POST http://100.107.221.118:8000/off/priz3
curl -X POST http://100.107.221.118:8000/on/priz3
curl http://100.107.221.118:8000/plugs
```

Veya `istek-gonder.bat` ile priz ID girip Enter'a basin.

## CLI

```powershell
python cli.py ac      # sadece ac
python cli.py kapat   # sadece kapat
python cli.py on
python cli.py off
python cli.py status
```

PowerShell kisayolu:

```powershell
.\tapo.ps1 ac
.\tapo.ps1 kapat
```

## Python projesinde kullanim

```python
from tapo_plug import TapoPlug

plug = TapoPlug.from_env()
plug.on()
plug.off()
print(plug.is_on())
```

## Test

```powershell
pip install -e ".[dev]"
pytest -v
```

Entegrasyon rehberi: [INTEGRATION.md](INTEGRATION.md)
