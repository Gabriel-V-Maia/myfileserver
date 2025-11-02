function Ensure-Admin {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Host "Reiniciando com privilégios de administrador..."
        Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
        exit
    }
}

Ensure-Admin

$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$Client = Join-Path $Root 'client'
$Server = Join-Path $Root 'server'
$ClientDist = Join-Path $Client 'dist'
$ServerDist = Join-Path $Server 'dist'

$ConfigRoot = Join-Path $env:USERPROFILE 'myfileserverconfigs'
$BinPath = Join-Path $ConfigRoot 'bins'
$EnvFile = Join-Path $ConfigRoot '.env'

Write-Host "criando estrutura de diretórios..."
if (-not (Test-Path $ConfigRoot)) { New-Item -ItemType Directory -Path $ConfigRoot -Force | Out-Null }
if (-not (Test-Path $BinPath)) { New-Item -ItemType Directory -Path $BinPath -Force | Out-Null }

Write-Host "tentando instalar dependências..."
python -m pip install --user pyinstaller python-dotenv

Write-Host "Compilando cliente..."
Push-Location $Client
python -m PyInstaller --onefile filepull.py --name pull
python -m PyInstaller --onefile filepush.py --name push
python -m PyInstaller --onefile filesend.py --name send
Pop-Location

Write-Host "Compilando servidor..."
Push-Location $Server
python -m PyInstaller --onefile server.py
Pop-Location

Write-Host "Copiando executáveis..."
Copy-Item (Join-Path $ClientDist 'pull.exe') $BinPath -Force
Copy-Item (Join-Path $ClientDist 'push.exe') $BinPath -Force
Copy-Item (Join-Path $ClientDist 'send.exe') $BinPath -Force
Copy-Item (Join-Path $ServerDist 'server.exe') $BinPath -Force

if (-not (Test-Path $EnvFile)) {
    Write-Host "`nConfiguração do servidor:"
    $serverIp = Read-Host "Digite o IP do servidor (ex: 192.168.1.100)"
    
    [System.IO.File]::WriteAllText($EnvFile, "server_ip=$serverIp`n", [System.Text.UTF8Encoding]::new($false))
    Write-Host "Arquivo .env criado em: $EnvFile" -ForegroundColor Green
} else {
    Write-Host "Arquivo .env já existe em: $EnvFile" -ForegroundColor Yellow
    Write-Host "Para reconfigurar, delete o arquivo e execute novamente." -ForegroundColor Yellow
}

function Test-Admin {
    ([Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
        [Security.Principal.WindowsBuiltInRole]::Administrator)
}

$scope = if (Test-Admin) { 'Machine' } else { 'User' }
$currentPath = [Environment]::GetEnvironmentVariable('Path', $scope).Split(';') | ForEach-Object { $_.Trim() }

if (-not ($currentPath -contains $BinPath)) {
    Write-Host "Adicionando ao PATH..."
    $newPath = ($currentPath + $BinPath) -join ';'
    [Environment]::SetEnvironmentVariable('Path', $newPath, $scope)
    $env:Path += ";$BinPath"
    Write-Host "PATH atualizado!" -ForegroundColor Green
}

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "Instalação concluída com sucesso!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "`nComandos disponíveis:"
Write-Host "  - pull <arquivo>" -ForegroundColor Yellow
Write-Host "  - push <arquivo1> <arquivo2> ..." -ForegroundColor Yellow
Write-Host "  - send <arquivo> <destinatario>" -ForegroundColor Yellow
Write-Host "  - server" -ForegroundColor Yellow
Write-Host "`nConfiguração em: $ConfigRoot" -ForegroundColor Cyan
Write-Host "`nOBS: Reinicie o terminal para usar os comandos!" -ForegroundColor Magenta

Read-Host "`nPressione Enter para sair"
