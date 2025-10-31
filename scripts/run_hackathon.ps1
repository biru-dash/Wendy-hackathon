# PowerShell script to run the Hackathon UI and ADK server
# This opens two separate PowerShell windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Wendy's Hackathon - Starting Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start ADK API Server in new window
Write-Host "Starting ADK API Server in new window..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$projectRoot'; .\venv\Scripts\Activate.ps1; adk api_server marketing_orchestrator"
)

Start-Sleep -Seconds 3

# Start Streamlit UI in new window
Write-Host "Starting Streamlit UI in new window..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$projectRoot'; .\venv\Scripts\Activate.ps1; streamlit run hackathon_ui.py"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Both servers are starting in separate windows." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "ADK API Server: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Streamlit UI: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

