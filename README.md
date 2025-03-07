# ImageCropper

## Overview
**ImageCropper** is a Python-based GUI application that resizes and crops images to specific print sizes at **300 DPI**. The tool ensures **center-cropping** to preserve important details and generates high-quality images for printing.

## Features
- Supports **multiple aspect ratios** for common print sizes (e.g., 16×20 inches for 4:5 ratio).
- Maintains **high resolution (300 DPI)** for professional-quality prints.
- **GUI interface** built with **Tkinter** for easy interaction.
- Uses **Pillow (PIL) for image processing**.
- Can be packaged into a standalone **executable file**.

---

## Setup & Installation

### **1️⃣ Automatic Setup (Recommended)**
#### **🔹 Windows**
1. Download python from official website https://www.python.org/downloads/
2. Install python and make sure to check the "Add to PATH" checkbox
3. **Download or clone** the repository.
4. **Run** `setup.bat` by double-clicking (DO NOT RUN AS ADMIN).
5. The script will:
   - Install all required dependencies (`pillow`, `tk`, `pyinstaller`).
   - Create an executable (`ImageCropper.exe`).
   - Clean up temporary files.
6. **After setup**, you can directly run `ImageCropper.exe`.

#### **🔹 Mac/Linux**
1. Open a terminal and **navigate** to the project folder:
   ```sh
   cd /path/to/ImageCropper
   ```
2. Make the setup script executable:
   ```sh
   chmod +x setup.sh
   ```
3. Run the script:
   ```sh
   ./setup.sh
   ```
4. The script will:
   - Install dependencies.
   - Generate an executable (`ImageCropper`).
   - Clean up unnecessary files.

---

### **2️⃣ Manual Setup (For Developers)**
If you prefer to run the script without creating an executable:

#### **🔹 Install Dependencies**
Make sure you have Python 3 installed, then run:
```sh
pip install pillow tk
```

#### **🔹 Run the Program**
```sh
python ImageCropper.py
```

---

## How to Use
1. Open the **ImageCropper GUI**.
2. **Select an input folder** containing images.
3. **Choose an output folder** where processed images will be saved.
4. Click **"Process Images"** to crop and resize images.
5. The processed images will be saved with **300 DPI** in the selected output folder.

---

## Build Your Own Executable (Optional)
If you modify the script and want to create a new executable:
```sh
python -m PyInstaller --onefile --noconfirm --noconsole --name "ImageCropper" ImageCropper.py
```

This will generate the **ImageCropper.exe** (Windows) or **ImageCropper** (Mac/Linux).

---

## ❓ Troubleshooting
### **🚫 "Python not found" error**
Ensure Python is installed and added to `PATH`. Check by running:
```sh
python --version
```

### **🚫 "Pillow/Tkinter not installed" error**
Manually install dependencies:
```sh
pip install pillow tk
```

### **🚫 Running as Admin moves the script to C:\Windows\System32**
**Solution:** Always run `setup.bat` normally, not as admin. If needed, manually navigate to the correct directory:
```sh
cd C:\Path\To\ImageCropper
setup.bat
```

