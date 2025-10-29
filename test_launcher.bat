@echo off
REM Quick Schemathesis Testing Launcher for Windows
REM This batch file provides easy access to Schemathesis testing

echo.
echo 🧪 Karyawan ^& Kantor API - Schemathesis Test Launcher
echo ===============================================
echo.

:menu
echo Choose testing option:
echo.
echo 1. Full Docker + Schemathesis Integration Test (Recommended)
echo 2. Standalone Schemathesis Test (API must be running)
echo 3. Validate Docker Setup Only
echo 4. Manual PowerShell Test Scripts
echo 5. View Test Documentation
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto docker_schemathesis
if "%choice%"=="2" goto standalone_schemathesis
if "%choice%"=="3" goto validate_docker
if "%choice%"=="4" goto manual_tests
if "%choice%"=="5" goto documentation
if "%choice%"=="6" goto exit
echo Invalid choice, please try again.
goto menu

:docker_schemathesis
echo.
echo 🐳 Running Full Docker + Schemathesis Integration Test...
echo This will build containers and run comprehensive API testing.
echo.
powershell.exe -ExecutionPolicy Bypass -File "docker_with_schemathesis.ps1"
goto end

:standalone_schemathesis
echo.
echo 🧪 Running Standalone Schemathesis Test...
echo Make sure your API is running at http://localhost:8080
echo.
powershell.exe -ExecutionPolicy Bypass -File "run_schemathesis_tests.ps1"
goto end

:validate_docker
echo.
echo 🔍 Validating Docker Setup...
echo.
bash validate-docker.sh
goto end

:manual_tests
echo.
echo 📋 Available Manual Test Scripts:
echo.
echo 1. Test Karyawan API
echo 2. Test Kantor API  
echo 3. Test All APIs
echo 4. Test Relationships
echo 5. Test Validation
echo 6. Back to main menu
echo.
set /p test_choice="Choose test script (1-6): "

if "%test_choice%"=="1" powershell.exe -ExecutionPolicy Bypass -File "test_karyawan_api.ps1"
if "%test_choice%"=="2" powershell.exe -ExecutionPolicy Bypass -File "test_kantor_simple.ps1"
if "%test_choice%"=="3" powershell.exe -ExecutionPolicy Bypass -File "test_all_apis.ps1"
if "%test_choice%"=="4" powershell.exe -ExecutionPolicy Bypass -File "test_relationships.ps1"
if "%test_choice%"=="5" powershell.exe -ExecutionPolicy Bypass -File "test_validation.ps1"
if "%test_choice%"=="6" goto menu

goto end

:documentation
echo.
echo 📚 Opening Test Documentation...
echo.
echo Available documentation files:
echo - README.md (Main project documentation)
echo - SCHEMATHESIS_GUIDE.md (Comprehensive testing guide)
echo - DATABASE_SETUP.md (Database setup guide)
echo - DOCKER_README.md (Docker deployment guide)
echo.
echo Opening SCHEMATHESIS_GUIDE.md...
start SCHEMATHESIS_GUIDE.md
goto end

:end
echo.
echo Press any key to return to menu or Ctrl+C to exit...
pause >nul
goto menu

:exit
echo.
echo Thanks for using Schemathesis Test Launcher! 🚀
echo.
exit /b 0