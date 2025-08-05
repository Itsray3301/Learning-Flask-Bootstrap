@echo off
echo 🌡️ Temperature Converter Web App - Development Server
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python tidak terinstall. Silakan install Python terlebih dahulu.
    pause
    exit /b 1
)

echo ✅ Python terdeteksi

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Flask belum terinstall. Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Gagal menginstall dependencies
        pause
        exit /b 1
    )
) else (
    echo ✅ Flask sudah terinstall
)

echo.
echo 🚀 Starting development server...
echo 📍 URL: http://localhost:5000
echo 🔧 Debug mode: ON
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

python app.py

pause