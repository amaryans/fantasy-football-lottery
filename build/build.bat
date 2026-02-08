@echo off
REM Build script for Fantasy Football Lottery Application
REM This script creates a standalone Windows executable

echo ========================================
echo Fantasy Football Lottery - Build Script
echo ========================================
echo.

REM Save current directory and move to project root
cd /d "%~dp0.."

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
python -m pip install -r build\requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Cleaning previous build...
if exist build_output rmdir /s /q build_output
if exist dist rmdir /s /q dist

echo.
echo [3/4] Building executable with PyInstaller...
python -m PyInstaller build\fantasy_football_lottery.spec --clean
if %errorlevel% neq 0 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo Executable location: dist\FantasyFootballLottery\FantasyFootballLottery.exe
echo ========================================
echo.
echo You can now:
echo 1. Run the executable from dist\FantasyFootballLottery\
echo 2. Copy the entire FantasyFootballLottery folder to distribute
echo.

pause
