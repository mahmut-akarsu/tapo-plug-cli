@echo off
title Tapo Istek Gonder
cd /d "%~dp0"

set API_HOST=100.107.221.118
set API_PORT=8000

echo.
echo Mevcut prizler: priz2, priz3, priz4
echo.
set /p PLUG_ID=Priz ID girin (ornek priz3): 
if "%PLUG_ID%"=="" (
    echo HATA: Priz ID bos olamaz.
    pause
    exit /b 1
)

echo.
echo [%PLUG_ID%] kapatma istegi gonderiliyor...
curl -s -X POST http://%API_HOST%:%API_PORT%/off/%PLUG_ID%
echo.
echo.
pause
