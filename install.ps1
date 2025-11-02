function Ensure-Admin {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Host "Reiniciando com privilégios de administrador..."
        Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
        exit
    }
}

Ensure-Admin

$Root        = Split-Path -Parent $MyInvocation.MyCommand.Definition
$Client      = Join-Path $Root 'client'
$Server      = Join-path $Root 'server'
$Dist        = Join-Path $Client 'dist'
$InstallRoot = Join-Path $env:ProgramFiles 'myfileserver'
$BinPath     = Join-Path $InstallRoot 'bin'

if (-not (Test-Path $BinPath)) {
    New-Item -ItemType Directory -Path $BinPath -Force | Out-Null
}

python -m pip install --user pyinstaller

Push-Location $Client
python -m PyInstaller --onefile pull.py
python -m PyInstaller --onefile push.py
python -m PyInstaller --onefile send.py
Pop-Location

Push-Location $Server
python -m PyInstaller --onefile server.py
Pop-Location

if (-not (Test-Path (Join-Path $Dist 'pull.exe'))) {
    Write-Host "Erro: não foi possível encontrar pull.exe"
    exit 1
}

Copy-Item (Join-Path $Dist 'pull.exe') $BinPath -Force
Copy-Item (Join-Path $Dist 'push.exe') $BinPath -Force
Copy-Item (Join-Path $Dist 'send.exe') $BinPath -Force

Copy-Item (Join-Path $Dist 'server.exe') $BinPath -Force

function Test-Admin {
    ([Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
        [Security.Principal.WindowsBuiltInRole]::Administrator)
}

$scope = if (Test-Admin) { 'Machine' } else { 'User' }
$currentPath = [Environment]::GetEnvironmentVariable('Path', $scope)

if (-not ($currentPath.Split(';') -contains $BinPath)) {
    [Environment]::SetEnvironmentVariable('Path', ($currentPath + ';' + $BinPath).TrimEnd(';'), $scope)
}

if (-not ($env:Path.Split(';') -contains $BinPath)) {
    $env:Path += ';' + $BinPath
}

Write-Host "`nTudo pronto!"
Read-Host "Pressione Enter para sair"

