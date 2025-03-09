#!/bin/bash

# Ensure script runs in its own directory, even if run from another location
cd "$(dirname "$0")"

echo "----------------------------------------"
echo "Current working directory: $(pwd)"
echo "Expected location for ImageCropper.py: $(pwd)/ImageCropper.py"
echo "----------------------------------------"

# CHECK IF ImageCropper.py EXISTS
if [ ! -f "$(pwd)/ImageCropper.py" ]; then
    echo "ERROR: ImageCropper.py not found!"
    echo "Please make sure this script is in the same folder as ImageCropper.py."
    exit 1
fi

# CLEANUP OLD BUILDS
echo "Cleaning up old builds..."
rm -rf venv dist build ImageCropper.spec

# CREATE VIRTUAL ENVIRONMENT
echo "Creating virtual environment..."
python3 -m venv venv

# ACTIVATE VENV AND INSTALL DEPENDENCIES
echo "Installing dependencies..."
source venv/bin/activate
python3 -m pip install --upgrade pip==23.3.1
python3 -m pip install pyinstaller==6.3.0 pillow tk

# BUILD EXECUTABLE
echo "Building executable..."
python3 -m PyInstaller \
    --onefile \
    --noconfirm \
    --noconsole \
    --name "ImageCropper" \
    ImageCropper.py

# MOVE EXECUTABLE TO MAIN FOLDER
if [ -f "dist/ImageCropper" ]; then
    echo "Moving executable to main folder..."
    mv dist/ImageCropper ./
else
    echo "ERROR: Executable not found! PyInstaller might have failed."
    exit 1
fi

# CLEANUP
echo "Cleaning up build directories..."
rm -rf dist build ImageCropper.spec

echo "----------------------------------------"
echo "BUILD SUCCESSFUL!"
echo "Executable: $(pwd)/ImageCropper"
echo "----------------------------------------"
