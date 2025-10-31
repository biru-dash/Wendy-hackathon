@echo off
REM Batch script to run the Hackathon UI and ADK server
REM This opens two separate command prompts

echo ========================================
echo Wendy's Hackathon - Starting Servers
echo ========================================
echo.

echo Starting ADK API Server in new window...
start "ADK API Server" cmd /k "cd /d %~dp0 && .\venv\Scripts\activate && adk api_server marketing_orchestrator"

timeout /t 3 /nobreak >nul

echo Starting Streamlit UI in new window...
start "Streamlit UI" cmd /k "cd /d %~dp0 && .\venv\Scripts\activate && streamlit run hackathon_ui.py"

echo.
echo ========================================
echo Both servers are starting in separate windows.
echo ========================================
echo.
echo ADK API Server: http://localhost:8000
echo Streamlit UI: http://localhost:8501
echo.
echo Close this window when done.
pause

