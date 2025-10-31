# ADK Web Server Management Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ADK Web Server Manager" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if ADK web is already running
$process = Get-Process | Where-Object { $_.ProcessName -eq "python" -or $_.ProcessName -eq "pythonw" } | Where-Object { 
    try { (Get-WmiObject Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine -like "*adk*web*" } 
    catch { $false }
}

if ($process) {
    Write-Host "ADK Web Server is RUNNING" -ForegroundColor Green
    Write-Host "Process ID: $($process.Id)" -ForegroundColor Yellow
    Write-Host "Open: http://127.0.0.1:8000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "1. Keep running (do nothing)"
    Write-Host "2. Stop and restart"
    Write-Host ""
    $choice = Read-Host "Enter choice (1 or 2)"
    
    if ($choice -eq "2") {
        Write-Host "Stopping process..." -ForegroundColor Yellow
        Stop-Process -Id $process.Id -Force
        Start-Sleep -Seconds 2
    } else {
        exit
    }
} else {
    Write-Host "ADK Web Server is NOT running" -ForegroundColor Red
    Write-Host ""
    Write-Host "Starting ADK Web Server..." -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting server at http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
cd $PSScriptRoot
venv\Scripts\python.exe -m adk web


