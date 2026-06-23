# Kullanim: .\tapo.ps1 ac | kapat | on | off | status
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet("on", "off", "ac", "kapat", "toggle", "status")]
    [string]$Command
)

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    & $venvPython cli.py $Command
} else {
    python cli.py $Command
}

exit $LASTEXITCODE
