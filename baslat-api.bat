@echo off
title Tapo Plug API
cd /d "%~dp0"

if not exist ".env" (
    echo HATA: .env dosyasi bulunamadi.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Tapo Plug API calisiyor
echo   Port: 8000
echo   POST /on/priz3   - priz ac
echo   POST /off/priz3  - priz kapat
echo   GET  /plugs      - priz listesi
echo ========================================
echo.
echo Kapatmak icin bu pencereyi kapat veya Ctrl+C
echo.

python -m uvicorn api:app --host 0.0.0.0 --port 8000

pause
