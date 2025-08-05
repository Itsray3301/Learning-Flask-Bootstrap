@echo off
echo 🧪 Temperature Converter Web App - Running Tests
echo ===============================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python tidak terinstall
    pause
    exit /b 1
)

REM Check if required modules are installed
python -c "import flask, unittest" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Installing test dependencies...
    pip install -r requirements.txt
)

echo.
echo 🧪 Running unit tests...
echo.

REM Run tests with coverage if available
python -c "import coverage" >nul 2>&1
if %errorlevel% equ 0 (
    echo 📊 Running tests with coverage...
    coverage run -m pytest test_web_app.py -v
    echo.
    echo 📈 Coverage Report:
    coverage report
) else (
    echo 🔍 Running basic tests...
    python test_web_app.py
)

echo.
echo ✅ Tests completed!
pause