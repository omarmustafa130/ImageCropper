@echo off
:: Get the directory of this script, even if run as Admin
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo ----------------------------------------
echo Current working directory: %CD%
echo Expected location for ImageCropperV2.py: %CD%\ImageCropper.py
echo ----------------------------------------

:: CHECK IF ImageCropper.py EXISTS
if not exist "%CD%\ImageCropperV2.py" (
    echo ERROR: ImageCropperV2.py not found!
    echo Please make sure this script is in the same folder as ImageCropperV2.py.
    pause
    exit /b
)

:: CLEANUP OLD BUILDS
echo Cleaning old builds...
rmdir /s /q .\venv 2>nul
rmdir /s /q .\dist 2>nul
rmdir /s /q .\build 2>nul
del *.spec 2>nul

:: CREATE VIRTUAL ENVIRONMENT
echo Creating virtual environment...
python -m venv venv

:: ACTIVATE VENV AND INSTALL DEPENDENCIES
echo Installing dependencies...
call .\venv\Scripts\activate.bat
python -m pip install --upgrade pip==23.3.1
python -m pip install pyinstaller==6.3.0 pillow tk

:: BUILD EXECUTABLE
echo Building executable...
python -m PyInstaller ^
    --onefile ^
    --noconfirm ^
    --noconsole ^
    --name "ImageCropperV2" ^
    ImageCropperV2.py

:: MOVE EXECUTABLE TO MAIN FOLDER
if exist "dist\ImageCropperV2.exe" (
    echo Moving executable to main folder...
    move /Y "dist\ImageCropperV2.exe" .
) else (
    echo ERROR: Executable not found! PyInstaller might have failed.
    pause
    exit /b
)

:: CLEANUP
echo Cleaning up...
rmdir /s /q "%CD%\build" 2>nul
rmdir /s /q "%CD%\dist" 2>nul
del /q *.spec 2>nul

echo ----------------------------------------
echo BUILD SUCCESSFUL!
echo Executable: %CD%\ImageCropperV2.exe
echo ----------------------------------------
pause
