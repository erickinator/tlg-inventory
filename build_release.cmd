@echo off
setlocal enabledelayedexpansion

:: === CONFIG ===
set PY_FILE=TLG_Inventory.pyw
set ICON=tlg.ico
set DIST_FOLDER=dist
set OUTPUT_FOLDER=release
set DEPLOY_FOLDER=G:\My Drive\Software-Distribution\TLG

:: === CLEAN OLD BUILD (optional) ===
if exist build (rmdir /s /q build)
if exist dist (rmdir /s /q dist)
if exist %PY_FILE:.pyw=.spec% (del %PY_FILE:.pyw=.spec%)

:: === BUILD EXE WITH PYINSTALLER ===
echo.
echo === [1/4] Building EXE ===
pyinstaller --noconfirm --onefile --windowed --icon "%ICON%" "%PY_FILE%"
if errorlevel 1 (
    echo Build failed. Aborting.
    pause
    exit /b 1
)

:: === MAKE ZIP ===
echo.
echo === [2/4] Creating ZIP Package ===
call make_zip.bat
if errorlevel 1 (
    echo make_zip.bat failed. Aborting.
    pause
    exit /b 1
)

:: === DEPLOY TO GOOGLE DRIVE ===
echo.
echo === [3/4] Deploying to Google Drive ===

if not exist "%DEPLOY_FOLDER%" (
    echo ERROR: Deploy folder does not exist: %DEPLOY_FOLDER%
    pause
    exit /b 1
)

:: Copy latest EXE
xcopy /Y "%DIST_FOLDER%\TLG Website Inventory.exe" "%DEPLOY_FOLDER%\"

:: Copy version.txt
xcopy /Y "%OUTPUT_FOLDER%\version.txt" "%DEPLOY_FOLDER%\"

:: Copy ZIP file
for %%F in (%OUTPUT_FOLDER%\TLG_Inventory_v*.zip) do (
    xcopy /Y "%%F" "%DEPLOY_FOLDER%\"
)

:: === DONE ===
echo.
echo === [4/4] Opening Deployment Folder ===
explorer "%DEPLOY_FOLDER%"

echo.
echo === Build and Deploy COMPLETE ===
pause
exit /b 0
