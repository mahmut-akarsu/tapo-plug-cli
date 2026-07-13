@echo off
cd /d "%~dp0"

if not exist ".env" exit /b 1
if not exist "logs" mkdir logs

start "" /B python -m uvicorn api:app --host 0.0.0.0 --port 8000 >> logs\api.log 2>&1
