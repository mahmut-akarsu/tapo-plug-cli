$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RemoteHost = "desktop-cnt7"
$RemoteIp = "100.107.221.118"
$RemoteDir = "C:\tapo-plug"
$ZipName = "tapo-plug-deploy.zip"
$ZipPath = Join-Path $ProjectRoot $ZipName

Write-Host "PC-7 durumu kontrol ediliyor..."
$ping = tailscale ping desktop-cnt7 2>&1 | Out-String
if ($ping -notmatch "pong from") {
    Write-Host "HATA: PC-7 ($RemoteIp) erisilemiyor."
    exit 1
}
Write-Host "PC-7 erisilebilir."

Write-Host "Deploy paketi hazirlaniyor..."
$staging = Join-Path $env:TEMP "tapo-plug-deploy"
if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging | Out-Null
New-Item -ItemType Directory -Path "$staging\tapo_plug" | Out-Null

Copy-Item "$ProjectRoot\api.py", "$ProjectRoot\api-servis.bat", "$ProjectRoot\baslat-api.bat", `
    "$ProjectRoot\kurulum.bat", "$ProjectRoot\istek-gonder.bat", "$ProjectRoot\requirements.txt", `
    "$ProjectRoot\.env" "$staging\"
Copy-Item "$ProjectRoot\tapo_plug\*.py" "$staging\tapo_plug\"

if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
Compress-Archive -Path "$staging\*" -DestinationPath $ZipPath -Force
Remove-Item $staging -Recurse -Force

Write-Host "PC-7'ye gonderiliyor..."
tailscale file cp $ZipPath "${RemoteHost}:"
if ($LASTEXITCODE -ne 0) { throw "Dosya gonderilemedi." }

Write-Host "PC-7'de kurulum calistiriliyor..."
$remoteCmd = @"
powershell -NoProfile -Command "
  New-Item -ItemType Directory -Path '$RemoteDir' -Force | Out-Null;
  Expand-Archive -Path `"`$env:USERPROFILE\$ZipName`" -DestinationPath '$RemoteDir' -Force;
  Remove-Item `"`$env:USERPROFILE\$ZipName`" -Force;
  Start-Process -FilePath '$RemoteDir\kurulum.bat' -WorkingDirectory '$RemoteDir'
"
"@

tailscale ssh $RemoteHost $remoteCmd
if ($LASTEXITCODE -ne 0) { throw "Uzaktan kurulum basarisiz." }

Write-Host "Bekleniyor (API ayaga kalksin)..."
Start-Sleep -Seconds 8

Write-Host "Uzak test: priz3 kapatma istegi..."
curl.exe -s -X POST "http://${RemoteIp}:8000/off/priz3"
Write-Host ""
curl.exe -s "http://${RemoteIp}:8000/health"
Write-Host ""
Write-Host "Deploy tamam."
