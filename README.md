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
