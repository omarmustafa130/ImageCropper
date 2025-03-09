#!/usr/bin/env python3
"""
GUI Image Resizer for Print Sizes at 300 DPI (Modernized)
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from PIL import Image

# Configuration for print sizes in inches (width, height)
TARGET_SIZES_INCHES = {
    (4, 5): (16, 20),   # 16x20 inches @300 DPI => 4800x6000 pixels
    (3, 4): (18, 24),   # 18x24 inches @300 DPI => 5400x7200 pixels
    (2, 3): (24, 36),   # 24x36 inches @300 DPI => 7200x10800 pixels
    (5, 7): (5, 7),     # 5x7 inches @300 DPI   => 1500x2100 pixels
}

DPI = 300  # Output resolution
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".bmp", ".webp")
JPEG_QUALITY = 95  # Higher quality for JPEG output

def center_crop_to_aspect_ratio(img, aspect_w, aspect_h):
    """
    Improved center-crop with accurate aspect ratio handling.
    """
    orig_w, orig_h = img.size
    target_ratio = aspect_w / aspect_h
    current_ratio = orig_w / orig_h

    if current_ratio > target_ratio:
        # Crop width
        new_width = int(orig_h * target_ratio)
        left = (orig_w - new_width) // 2
        return img.crop((left, 0, left + new_width, orig_h))
    else:
        # Crop height
        new_height = int(orig_w / target_ratio)
        top = (orig_h - new_height) // 2
        return img.crop((0, top, orig_w, top + new_height))

def process_images(input_folder, output_folder, log_func):
    """
    Enhanced processing with better error handling and quality controls.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(VALID_EXTENSIONS)]
    
    if not files:
        log_func("No valid image files found in input folder")
        return

    for filename in files:
        input_path = os.path.join(input_folder, filename)
        try:
            with Image.open(input_path) as img:
                base_name = os.path.splitext(filename)[0]
                log_func(f"\nProcessing: {filename}")
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                for (aspect_w, aspect_h), (in_w, in_h) in TARGET_SIZES_INCHES.items():
                    try:
                        # Calculate target dimensions
                        target_w = int(in_w * DPI)
                        target_h = int(in_h * DPI)
                        
                        # Center crop
                        cropped = center_crop_to_aspect_ratio(img, aspect_w, aspect_h)
                        
                        # High-quality resize
                        resized = cropped.resize((target_w, target_h), Image.LANCZOS)
                        
                        # Save settings
                        out_name = f"{base_name}_{aspect_w}x{aspect_h}_{in_w}x{in_h}in.jpg"
                        out_path = os.path.join(output_folder, out_name)
                        
                        # Save with quality and DPI settings
                        resized.save(
                            out_path, 
                            dpi=(DPI, DPI),
                            quality=JPEG_QUALITY,
                            optimize=True,
                            subsampling=0  # Best quality for JPEG
                        )
                        log_func(f"Saved: {out_name} ({target_w}x{target_h}px)")
                    except Exception as e:
                        log_func(f"Error processing {filename} for {aspect_w}:{aspect_h}: {str(e)}")
        except Exception as e:
            log_func(f"Failed to process {filename}: {str(e)}")
    
    log_func("\nProcessing complete. Check output folder.")

class ImageResizerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GUI Image Resizer for Print Sizes")
        self.geometry("615x550")
        self.resizable(False, False)

        # Use ttk's themed style for a modern look
        style = ttk.Style(self)
        style.theme_use('clam')

        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Main container frame
        container = ttk.Frame(self, padding=10)
        container.pack(fill="both", expand=True)

        # Input Folder Frame (using grid)
        frame_input = ttk.Frame(container)
        frame_input.grid(row=0, column=0, sticky="ew", pady=5)
        frame_input.columnconfigure(1, weight=1)

        ttk.Label(frame_input, text="Input Folder:   ").grid(row=0, column=0, sticky="w")
        self.input_entry = ttk.Entry(frame_input, textvariable=self.input_folder)
        self.input_entry.grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(frame_input, text="Browse", command=self.browse_input).grid(row=0, column=2, sticky="e")

        # Output Folder Frame
        frame_output = ttk.Frame(container)
        frame_output.grid(row=1, column=0, sticky="ew", pady=5)
        frame_output.columnconfigure(1, weight=1)

        ttk.Label(frame_output, text="Output Folder:").grid(row=0, column=0, sticky="w")
        self.output_entry = ttk.Entry(frame_output, textvariable=self.output_folder)
        self.output_entry.grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Button(frame_output, text="Browse", command=self.browse_output).grid(row=0, column=2, sticky="e")

        # Process Button Frame (centered)
        frame_button = ttk.Frame(container)
        frame_button.grid(row=2, column=0, sticky="ew", pady=10)
        frame_button.columnconfigure(0, weight=1)
        process_button = ttk.Button(frame_button, text="Process Images", command=self.start_processing)
        process_button.grid(row=0, column=0, sticky="")

        # Log area (scrolled text)
        self.log_area = scrolledtext.ScrolledText(container, width=70, height=20, state="disabled")
        self.log_area.grid(row=3, column=0, sticky="nsew", pady=10)
        container.rowconfigure(3, weight=1)

    def browse_input(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)

    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def start_processing(self):
        input_dir = self.input_folder.get()
        output_dir = self.output_folder.get()

        if not input_dir or not output_dir:
            messagebox.showwarning("Missing Folder", "Please select both input and output folders.")
            return

        # Clear log area
        self.log_area.config(state="normal")
        self.log_area.delete("1.0", tk.END)
        self.log_area.config(state="disabled")

        # Disable widgets during processing
        for widget in self.winfo_children():
            try:
                if "state" in widget.keys():
                    widget.config(state="disabled")
            except Exception:
                pass

        self.log("Starting image processing...")

        # Run the process in a separate thread to avoid freezing the GUI
        thread = threading.Thread(
            target=lambda: self.run_processing(input_dir, output_dir),
            daemon=True
        )
        thread.start()

    def run_processing(self, input_dir, output_dir):
        process_images(input_dir, output_dir, self.log)
        # Re-enable widgets after processing is complete
        self.after(0, self.enable_widgets)

    def enable_widgets(self):
        for widget in self.winfo_children():
            try:
                if "state" in widget.keys():
                    widget.config(state="normal")
            except Exception:
                pass
        messagebox.showinfo("Complete", "Image processing is complete.")

if __name__ == "__main__":
    app = ImageResizerGUI()
    app.mainloop()
