@echo off
TITLE NanoPro Operator — Autonomous GUI & Devin Engine
COLOR 0A

echo ===============================================================================
echo     🧠 NanoPro Operator: Autonomous GUI Computer-Use & Devin Engine
echo     4,804+ Frontier Models Mesh • Playwright & PyAutoGUI • Self-Healing
echo ===============================================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    pause
    exit /b
)

echo [2/3] Checking Playwright browser binaries...
playwright install chromium

echo [3/3] Launching NanoPro Split-Screen Dashboard UI...
echo Opening interactive dashboard at http://localhost:8501
echo.
python run_operator.py --ui

pause
