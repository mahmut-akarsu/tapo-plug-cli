Set-Location C:\tapo-plug
Start-Process "C:\Users\PC\AppData\Local\Programs\Python\Python313\python.exe" `
  -ArgumentList "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000" `
  -WindowStyle Hidden
