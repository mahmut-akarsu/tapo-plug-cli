@echo off
title Tapo Plug API Kurulum
cd /d "%~dp0"

if not exist ".env" (
    echo HATA: .env dosyasi bulunamadi.
    pause
    exit /b 1
)

echo [1/5] Paketler kuruluyor...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo HATA: pip install basarisiz.
    pause
    exit /b 1
)

echo [2/5] Firewall kurali...
netsh advfirewall firewall add rule name=TapoPlugAPI dir=in action=allow protocol=TCP localport=8000 >nul 2>&1

echo [3/5] Otomatik baslatma gorevi...
schtasks /Delete /TN "TapoPlugAPI" /F >nul 2>&1
schtasks /Create /TN "TapoPlugAPI" /TR "%~dp0start-api.bat" /SC ONLOGON /RL HIGHEST /F
if errorlevel 1 (
    echo HATA: Zamanlanmis gorev olusturulamadi.
    pause
    exit /b 1
)

echo [4/5] API baslatiliyor...
call "%~dp0start-api.bat"

echo [5/5] Saglik kontrolu...
timeout /t 4 /nobreak >nul
curl -s http://127.0.0.1:8000/health
echo.
echo.
echo Kurulum tamam. Her acilista otomatik baslar.
pause
