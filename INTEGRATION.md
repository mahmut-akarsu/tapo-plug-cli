# Koalya Entegrasyon Rehberi

Tapo P100 priz kontrolu icin `tapo-plug-cli` kutuphanesinin Koalya projesine baglanmasi.

**Repo:** https://github.com/mahmut-akarsu/tapo-plug-cli

---

## 1. On kosullar

| Gereksinim | Aciklama |
|------------|----------|
| Cihaz | Tapo P100 (TPAP firmware destekli) |
| Ag | Koalya sunucusu/cihazi priz ile **aynı Wi-Fi** |
| Tapo hesabi | Uygulamaya giris e-posta + sifre |
| Tapo uygulamasi | **Ben → Third-Party Services → Third-Party Compatibility** acik |

---

## 2. Kurulum

### Secenek A — GitHub'dan (onerilen)

Koalya `requirements.txt` dosyasina ekleyin:

```txt
git+https://github.com/mahmut-akarsu/tapo-plug-cli.git@main
```

```powershell
pip install -r requirements.txt
```

(`tapo` ve `python-dotenv` bagimliliklari otomatik kurulur.)

### Secenek B — Yerel gelistirme

```powershell
pip install -e C:\path\to\tapo-plug-cli
```

---

## 3. Yapilandirma

Koalya proje kokune `.env` ekleyin (repoya commit etmeyin):

```env
TAPO_IP=192.168.1.162
TAPO_EMAIL=ornek@email.com
TAPO_PASSWORD=Tapo_hesap_sifresi
```

`.gitignore` icinde `.env` oldugundan emin olun.

---

## 4. Python entegrasyonu

### Minimal kullanim

```python
from tapo_plug import TapoPlug, TapoConnectionError, TapoConfigError

plug = TapoPlug.from_env()

plug.on()          # ac
plug.off()         # kapat
plug.is_on()       # True / False
plug.get_info()    # {"device_on": bool, "nickname": str | None}
```

### Koalya servis ornegi

```python
# koalya/services/tapo_service.py
from tapo_plug import TapoConfigError, TapoConnectionError, TapoPlug


class TapoService:
    def __init__(self) -> None:
        self._plug = TapoPlug.from_env()

    def ac(self) -> None:
        self._plug.on()

    def kapat(self) -> None:
        self._plug.off()

    def durum(self) -> bool:
        return self._plug.is_on()


def tapo_ac() -> None:
    try:
        TapoService().ac()
    except TapoConfigError as e:
        raise RuntimeError(f"Tapo yapilandirma hatasi: {e}") from e
    except TapoConnectionError as e:
        raise RuntimeError(f"Tapo baglanti hatasi: {e}") from e
```

### Parametre ile (`.env` kullanmadan)

```python
from tapo_plug import TapoPlug

plug = TapoPlug(
    ip=settings.TAPO_IP,
    email=settings.TAPO_EMAIL,
    password=settings.TAPO_PASSWORD,
)
plug.on()
```

---

## 5. CLI / subprocess entegrasyonu

Koalya shell veya baska dil kullaniyorsa:

```python
import subprocess

def tapo_kapat() -> None:
    result = subprocess.run(
        ["python", "cli.py", "kapat"],
        cwd="/path/to/tapo-plug-cli",
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
```

CLI komutlari:

| Komut | Islem |
|-------|--------|
| `python cli.py ac` | Sadece ac |
| `python cli.py kapat` | Sadece kapat |
| `python cli.py status` | Durum (JSON) |

---

## 6. Hata yonetimi

```python
from tapo_plug import TapoConfigError, TapoConnectionError

try:
    plug.on()
except TapoConfigError:
    # .env eksik veya hatali
    ...
except TapoConnectionError:
    # IP yanlis, Wi-Fi farkli, Third-Party Compatibility kapali
    ...
```

---

## 7. Test

```powershell
# Mock test (cihaz gerekmez)
pytest -v

# Gercek cihaz
python cli.py status
python cli.py kapat
python cli.py ac
```

---

## 8. Kontrol listesi

- [ ] `pip install` tamamlandi
- [ ] Koalya `.env` dosyasi dolu
- [ ] Tapo uygulamasinda Third-Party Compatibility acik
- [ ] `python cli.py status` calisiyor
- [ ] `TapoPlug.from_env().on()` / `.off()` Koalya icinden cagrildi

---

## API ozeti

| Sinif / metod | Aciklama |
|---------------|----------|
| `TapoPlug.from_env()` | `.env` dosyasindan olustur |
| `TapoPlug(ip=, email=, password=)` | Manuel olustur |
| `.on()` | Priz ac |
| `.off()` | Priz kapat |
| `.toggle()` | Durumu degistir |
| `.is_on()` | Acik mi? |
| `.get_info()` | Cihaz bilgisi |
