@echo off
echo 🧪 Temperature Converter - Menjalankan Test
echo ===============================================

REM Cek Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python belum terinstall
    pause
    exit /b 1
)

REM Cek module yang dibutuhkan
python -c "import flask, unittest" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Install dependencies untuk test...
    python -m pip install -r requirements.txt
)

echo.
echo 🧪 Menjalankan unit test...
echo.

REM Jalankan test dengan coverage jika ada
python -c "import coverage" >nul 2>&1
if %errorlevel% equ 0 (
    echo 📊 Menjalankan test dengan coverage...
    coverage run -m pytest test_web_app.py -v
    echo.
    echo 📈 Coverage Report:
    coverage report
) else (
    echo 🔍 Menjalankan test dasar...
    python test_web_app.py
)

echo.
echo ✅ Test selesai!
pause