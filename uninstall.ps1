function Ensure-Admin {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Host "Reiniciando com privilégios de administrador..."
        Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
        exit
    }
}

Ensure-Admin

$ConfigRoot = Join-Path $env:USERPROFILE 'myfileserverconfigs'
$BinPath = Join-Path $ConfigRoot 'bins'

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Desinstalando myfileserver..." -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan

function Test-Admin {
    ([Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
        [Security.Principal.WindowsBuiltInRole]::Administrator)
}

$scope = if (Test-Admin) { 'Machine' } else { 'User' }
$currentPath = [Environment]::GetEnvironmentVariable('Path', $scope).Split(';') | ForEach-Object { $_.Trim() }

if ($currentPath -contains $BinPath) {
    Write-Host "Removendo do PATH..."
    $newPath = ($currentPath | Where-Object { $_ -ne $BinPath }) -join ';'
    [Environment]::SetEnvironmentVariable('Path', $newPath, $scope)
    Write-Host "PATH atualizado!" -ForegroundColor Green
}

if (Test-Path $ConfigRoot) {
    Write-Host "Removendo diretório de configuração..."
    Remove-Item -Path $ConfigRoot -Recurse -Force
    Write-Host "Diretório removido: $ConfigRoot" -ForegroundColor Green
} else {
    Write-Host "Diretório de configuração não encontrado." -ForegroundColor Yellow
}

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "Desinstalação concluída!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan

Read-Host "`nPressione Enter para sair"
