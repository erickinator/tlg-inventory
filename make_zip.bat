@echo off
setlocal enabledelayedexpansion

:: === CONFIG ===
set DIST_FOLDER=dist
set OUTPUT_FOLDER=release
set BASE_NAME=TLG_Inventory

:: === READ VERSION FROM FILE ===
set VERSION=
for /f "usebackq tokens=* delims=" %%v in ("%DIST_FOLDER%\version.txt") do set VERSION=%%v
if "%VERSION%"=="" (
    echo ERROR: Could not read version from version.txt!
    pause
    exit /b 1
)

:: === PREP OUTPUT FOLDER ===
if not exist "%OUTPUT_FOLDER%" (
    mkdir "%OUTPUT_FOLDER%"
)

:: === DEFINE ZIP FILE NAME ===
set ZIP_FILE=%OUTPUT_FOLDER%\%BASE_NAME%_v%VERSION%.zip

:: === DELETE OLD ZIP ===
if exist "%ZIP_FILE%" del "%ZIP_FILE%"

:: === CREATE ZIP ===
powershell -Command "Compress-Archive -Path '%DIST_FOLDER%\*' -DestinationPath '%ZIP_FILE%'"

if exist "%ZIP_FILE%" (
    echo Successfully created zip: %ZIP_FILE%
) else (
    echo ZIP creation failed!
    pause
    exit /b 1
)
