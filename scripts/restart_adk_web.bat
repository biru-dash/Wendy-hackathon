@echo off
echo ============================================
echo ADK Web Server Restart
echo ============================================
echo.

REM Kill any existing processes on port 8000
echo Checking for existing servers on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM Wait a moment for processes to die
timeout /t 2 /nobreak >nul

REM Start the new server
echo.
echo ============================================
echo Starting ADK Web Server
echo ============================================
echo.
echo The web interface will be available at: http://127.0.0.1:8000
echo Press CTRL+C to stop the server
echo.
call venv\Scripts\activate.bat
venv\Scripts\adk.exe web


