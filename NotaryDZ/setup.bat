@echo off
setlocal enabledelayedexpansion

:: Ensure we are in the directory where the script is located
cd /d "%~dp0"

echo ==========================================
echo [1/4] Checking Python installation...
echo ==========================================

:: 1. Check if python is in PATH
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PY_CMD=python
    goto :found
)

:: 2. Check if 'py' launcher is in PATH
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PY_CMD=py
    goto :found
)

:: 3. Check common Windows installation paths (AppData)
set "LOCAL_PY=%LOCALAPPDATA%\Programs\Python"
if exist "%LOCAL_PY%" (
    for /f "delays=" %%i in ('dir /b /ad "%LOCAL_PY%\Python*"') do (
        if exist "%LOCAL_PY%\%%i\python.exe" (
            set "PY_CMD=%LOCAL_PY%\%%i\python.exe"
            goto :found
        )
    )
)

:: 4. Check Program Files
set "PROG_PY=%ProgramFiles%\Python"
if exist "%PROG_PY%" (
    for /f "delays=" %%i in ('dir /b /ad "%PROG_PY%\Python*"') do (
        if exist "%PROG_PY%\%%i\python.exe" (
            set "PY_CMD=%PROG_PY%\%%i\python.exe"
            goto :found
        )
    )
)

echo [ERROR] Python is installed but not found in common paths or PATH.
echo Please add Python to your Windows PATH manually.
pause
exit /b

:found
echo [INFO] Found Python at: %PY_CMD%

echo ==========================================
echo [2/4] Creating Virtual Environment (venv)...
echo ==========================================
if not exist venv (
    "%PY_CMD%" -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
) else (
    echo [INFO] Virtual environment already exists.
)

echo ==========================================
echo [3/4] Installing dependencies in venv...
echo ==========================================
if not exist requirements.txt (
    echo [ERROR] requirements.txt not found in %CD%
    pause
    exit /b
)

call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b
)

echo ==========================================
echo [4/4] Building the application (.exe)...
echo ==========================================
if not exist main.py (
    echo [ERROR] main.py not found in %CD%
    pause
    exit /b
)

pip install pyinstaller
pyinstaller --noconsole --onefile --name "NotaryDZ_AI" main.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build the application.
    pause
    exit /b
)

echo ==========================================
echo [DONE] Success!
echo The application is in the 'dist' folder: NotaryDZ_AI.exe
echo ==========================================
pause
