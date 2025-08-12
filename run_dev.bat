@echo off
echo 🌡️ Temperature Converter - Server Development
echo ================================================

REM Cek apakah Python sudah terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python belum terinstall. Install Python dulu ya!
    pause
    exit /b 1
)

echo ✅ Python terdeteksi

REM Cek apakah Flask sudah terinstall
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Flask belum ada. Sedang install dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Gagal install dependencies
        pause
        exit /b 1
    )
) else (
    echo ✅ Flask sudah terinstall
)

echo.
echo 🚀 Menjalankan server development...
echo 📍 URL: http://localhost:5000
echo 🔧 Mode debug: AKTIF
echo.
echo Tekan Ctrl+C untuk stop server
echo ================================================
echo.

python app.py

pause