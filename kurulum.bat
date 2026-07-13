@echo off
title Tapo Plug API Kurulum
cd /d "%~dp0"

if not exist ".env" (
    echo HATA: .env dosyasi bulunamadi.
    pause
    exit /b 1
)

echo [1/4] Paketler kuruluyor...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo HATA: pip install basarisiz.
    pause
    exit /b 1
)

echo [2/4] Otomatik baslatma gorevi olusturuluyor...
schtasks /Delete /TN "TapoPlugAPI" /F >nul 2>&1
schtasks /Create /TN "TapoPlugAPI" /TR "cmd /c \"\"%~dp0api-servis.bat\"\"" /SC ONLOGON /RL HIGHEST /F
if errorlevel 1 (
    echo HATA: Zamanlanmis gorev olusturulamadi. Yonetici olarak calistirin.
    pause
    exit /b 1
)

echo [3/4] API baslatiliyor...
if not exist "logs" mkdir logs
start "" /MIN cmd /c "%~dp0api-servis.bat"

echo [4/4] Saglik kontrolu...
timeout /t 4 /nobreak >nul
curl -s http://127.0.0.1:8000/health
echo.
echo.
echo Kurulum tamam.
echo - API port: 8000
echo - Her Windows acilisinda otomatik baslar
echo - Log: logs\api.log
echo.
pause
