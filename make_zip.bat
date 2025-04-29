@echo off
setlocal enabledelayedexpansion

:: ==== Config ====
set DIST_FOLDER=dist
set OUTPUT_FOLDER=release
set PY_FILE=TLG_Inventory.pyw

:: ==== Extract version from Python file ====
for /f "tokens=2 delims== " %%a in ('findstr /b /c:"APP_VERSION =" "%PY_FILE%"') do (
    set VERSION=%%~a
)

:: Remove any quotes from version string
set VERSION=%VERSION:"=%

set ZIP_NAME=TLG_Inventory_v%VERSION%.zip

:: ==== Ensure output folder exists ====
if not exist %OUTPUT_FOLDER% (
    mkdir %OUTPUT_FOLDER%
)

:: ==== Write version.txt ====
echo %VERSION%> %OUTPUT_FOLDER%\version.txt

:: ==== Clean old ZIP if exists ====
if exist %OUTPUT_FOLDER%\%ZIP_NAME% (
    del %OUTPUT_FOLDER%\%ZIP_NAME%
)

:: ==== Create ZIP ====
echo Creating package: %ZIP_NAME%
powershell Compress-Archive -Path %DIST_FOLDER%\* -DestinationPath %OUTPUT_FOLDER%\%ZIP_NAME%

echo.
echo Done.
echo.
echo Version: %VERSION%
echo ZIP located at: %OUTPUT_FOLDER%\%ZIP_NAME%
echo version.txt created at: %OUTPUT_FOLDER%\version.txt
pause
