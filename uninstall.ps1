function Ensure-Admin {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
        Write-Host "Reiniciando com privilégios de administrador..."
        Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`""
        exit
    }
}

Ensure-Admin

$InstallRoot = Join-Path $env:ProgramFiles 'myfileserver'
$BinPath     = Join-Path $InstallRoot 'bin'

function Test-Admin {
    ([Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
        [Security.Principal.WindowsBuiltInRole]::Administrator)
}

$scope = if (Test-Admin) { 'Machine' } else { 'User' }

if (Test-Path $BinPath) {
    Remove-Item -Path $BinPath -Recurse -Force
}

if (Test-Path $InstallRoot) {
    Remove-Item -Path $InstallRoot -Recurse -Force
}

$currentPath = [Environment]::GetEnvironmentVariable('Path', $scope)
$newPath = ($currentPath.Split(';') | Where-Object { $_ -ne $BinPath }) -join ';'

[Environment]::SetEnvironmentVariable('Path', $newPath, $scope)

Write-Host "`nDesinstalação completa!"
Read-Host "Pressione Enter para sair"
