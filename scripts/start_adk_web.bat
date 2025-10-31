@echo off
echo ============================================
echo Starting ADK Web Server
echo ============================================
echo.
echo The web interface will be available at: http://127.0.0.1:8000
echo Press CTRL+C to stop the server
echo.
call venv\Scripts\activate.bat
python -m adk web
pause


