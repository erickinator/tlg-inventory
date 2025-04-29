@echo off
setlocal enabledelayedexpansion

:: === CONFIG ===
set PY_FILE=TLG_Inventory.pyw
set ICON=tlg.ico
set DIST_FOLDER=dist
set OUTPUT_FOLDER=release
set DEPLOY_FOLDER=G:\My Drive\Software-Distribution\TLG
set BASE_NAME=TLG_Inventory

:: === CLEAN OLD BUILD ===
echo Cleaning build and dist folders...
if exist build (rmdir /s /q build)
if exist dist (rmdir /s /q dist)
if exist "%PY_FILE:.pyw=.spec%" (del "%PY_FILE:.pyw=.spec%")

:: === BUILD EXE ===
echo.
echo === [1/4] Building EXE ===
pyinstaller --noconfirm --onefile --windowed --icon="%ICON%" "%PY_FILE%"
if errorlevel 1 (
    echo Build failed. Aborting.
    pause
    exit /b 1
)

:: === COPY STATIC FILES INTO DIST ===
echo.
echo === [2/4] Copying support files to dist ===
xcopy /Y ".\logo.png" "%DIST_FOLDER%\"
xcopy /Y ".\readme.txt" "%DIST_FOLDER%\"
xcopy /Y ".\readme.html" "%DIST_FOLDER%\"
xcopy /Y ".\version.txt" "%DIST_FOLDER%\"
xcopy /Y ".\tlg.ico" "%DIST_FOLDER%\"
xcopy /Y ".\config.json" "%DIST_FOLDER%\" >nul 2>&1

:: === READ VERSION FROM FILE ===
set VERSION=
for /f "usebackq tokens=* delims=" %%v in ("%DIST_FOLDER%\version.txt") do set VERSION=%%v
if "%VERSION%"=="" (
    echo ERROR: version.txt not found or empty.
    pause
    exit /b 1
)
set ZIP_NAME=%BASE_NAME%_v%VERSION%.zip

:: === MAKE ZIP PACKAGE ===
echo.
echo === [3/4] Creating ZIP Package ===
call make_zip.bat
if errorlevel 1 (
    echo make_zip.bat failed. Aborting.
    pause
    exit /b 1
)

:: === DEPLOY TO GOOGLE DRIVE ===
echo.
echo === [4/4] Deploying to Google Drive ===

if not exist "%DEPLOY_FOLDER%" (
    echo ERROR: Deploy folder does not exist: %DEPLOY_FOLDER%
    pause
    exit /b 1
)

xcopy /Y "%DIST_FOLDER%\%BASE_NAME%.exe" "%DEPLOY_FOLDER%\"
xcopy /Y "%DIST_FOLDER%\version.txt" "%DEPLOY_FOLDER%\"
xcopy /Y "%OUTPUT_FOLDER%\%ZIP_NAME%" "%DEPLOY_FOLDER%\"

:: === DONE ===
echo.
echo === Build and Deploy COMPLETE ===
explorer "%DEPLOY_FOLDER%"
pause
exit /b 0
