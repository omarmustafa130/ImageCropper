import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageTk

DPI = 300
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".bmp", ".webp")
JPEG_QUALITY = 95

RATIO_DIMENSIONS = {
    "1:1": [(5, 5), (8, 8), (10, 10), (12, 12), (16, 16), (20, 20), (24, 24), (30, 30), (36, 36)],
    "4:5": [(4, 5), (8, 10), (11, 14), (16, 20), (20, 25), (24, 30), (32, 40)],
    "2:3": [(2, 3), (4, 6), (8, 12), (12, 18), (16, 24), (20, 30), (24, 36), (30, 45)],
    "3:4": [(3, 4), (6, 8), (9, 12), (12, 16), (18, 24), (24, 32), (30, 40)],
    "5:7": [(5, 7), (10, 14), (15, 21), (20, 28), (25, 35), (30, 42)],
    "16:9": [(16, 9), (32, 18), (48, 27), (64, 36)],
    "9:16": [(9, 16), (18, 32), (27, 48), (36, 64)],
    "16:10": [(16, 10), (32, 20), (48, 30), (64, 40)]
}
class ImageResizerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GUI Image Resizer for Print Sizes")
        self.geometry("850x750")
        self.resizable(False, False)

        self.input_folder = tk.StringVar()
        self.input_file = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.selected_ratios = []
        self.dimensions_map = {}
        self.manual_crop_mode = False
        self.crop_x = None
        self.crop_y = None

        self.create_widgets()

    def create_widgets(self):
        container = ttk.Frame(self, padding=10)
        container.pack(fill="both", expand=True)

        # Input Selection
        frame_input = ttk.LabelFrame(container, text="Input Selection")
        frame_input.pack(fill="x", pady=5)

        # Folder selection
        frame_folder = ttk.Frame(frame_input)
        frame_folder.pack(fill="x", pady=2)
        ttk.Button(frame_folder, text="Select Folder", command=self.browse_input_folder).pack(side="left")
        ttk.Label(frame_folder, textvariable=self.input_folder, width=70).pack(side="left", padx=5)

        # File selection
        frame_file = ttk.Frame(frame_input)
        frame_file.pack(fill="x", pady=2)
        ttk.Button(frame_file, text="Select File", command=self.browse_input_file).pack(side="left")
        ttk.Label(frame_file, textvariable=self.input_file, width=80).pack(side="left", padx=5)

        # Output Folder
        frame_output = ttk.LabelFrame(container, text="Output Folder")
        frame_output.pack(fill="x", pady=5)
        ttk.Entry(frame_output, textvariable=self.output_folder, width=120).pack(side="left", padx=5)
        ttk.Button(frame_output, text="Browse", command=self.browse_output).pack(side="left")

        # Ratio and Dimensions
        frame_ratio_dim = ttk.LabelFrame(container, text="Select Aspect Ratios and Dimensions")
        frame_ratio_dim.pack(fill="x", pady=5)

        self.ratio_var = tk.StringVar()
        self.dimension_var = tk.StringVar()

        ttk.Label(frame_ratio_dim, text="Aspect Ratio:").pack(side="left", padx=5)
        self.ratio_dropdown = ttk.Combobox(frame_ratio_dim, textvariable=self.ratio_var, state="readonly", width=12)
        self.ratio_dropdown.pack(side="left", padx=5)
        self.ratio_dropdown["values"] = list(RATIO_DIMENSIONS.keys())
        self.ratio_dropdown.bind("<<ComboboxSelected>>", self.update_dimensions)

        ttk.Label(frame_ratio_dim, text="Dimensions:").pack(side="left", padx=5)
        self.dimension_dropdown = ttk.Combobox(frame_ratio_dim, textvariable=self.dimension_var, state="readonly", width=15)
        self.dimension_dropdown.pack(side="left", padx=5)

        ttk.Button(frame_ratio_dim, text="Add", command=self.add_ratio_dimension).pack(side="left", padx=5)
        ttk.Button(frame_ratio_dim, text="Clear List", command=self.clear_ratio_dimensions).pack(side="left", padx=5)
        
        self.dimensions_display = tk.Listbox(frame_ratio_dim, height=8, width=40)
        self.dimensions_display.pack(fill="x", padx=5, pady=5)

        # Processing Options
        frame_options = ttk.LabelFrame(container, text="Processing Options")
        frame_options.pack(fill="x", pady=5)
        self.manual_crop_check = ttk.Checkbutton(frame_options, text="Enable Manual Crop", command=self.toggle_manual_crop)
        self.manual_crop_check.pack(side="left")
        self.manual_crop_check.state(["!alternate"])

        # Process Button
        ttk.Button(container, text="Process Images", command=self.start_processing).pack(pady=10)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(container, width=100, height=15, state="disabled")
        self.log_area.pack(padx=10, pady=10)


    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)

    def browse_input_file(self):
        file = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.tif;*.bmp;*.webp")])
        if file:
            self.input_file.set(file)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)

    def update_dimensions(self, event):
        selected_ratio = self.ratio_var.get()
        if selected_ratio in RATIO_DIMENSIONS:
            dims = [f"{w}x{h}" for w, h in RATIO_DIMENSIONS[selected_ratio]]
            self.dimension_dropdown["values"] = dims
            self.dimension_dropdown.current(0)

    def add_ratio_dimension(self):
        ratio = self.ratio_var.get()
        dimension = self.dimension_var.get()
        if ratio and dimension:
            if ratio not in self.dimensions_map:
                self.dimensions_map[ratio] = []
            self.dimensions_map[ratio].append(dimension)
            self.dimensions_display.insert(tk.END, f"{ratio} -> {dimension}")

    def toggle_manual_crop(self):
        self.manual_crop_mode = not self.manual_crop_mode

    def start_processing(self):
        if self.input_folder.get():
            self.process_folder()
        elif self.input_file.get():
            self.process_single_image()
        else:
            messagebox.showwarning("Missing Input", "Please select an input file or folder.")

    def process_folder(self):
        input_dir = self.input_folder.get()
        output_dir = self.output_folder.get()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        files = [f for f in os.listdir(input_dir) if f.lower().endswith(VALID_EXTENSIONS)]
        
        if not files:
            self.log("No valid image files found in input folder")
            return

        for filename in files:
            input_path = os.path.join(input_dir, filename)
            try:
                with Image.open(input_path) as img:
                    base_name = os.path.splitext(filename)[0]
                    self.log(f"\nProcessing: {filename}")

                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    for ratio, dimensions in self.dimensions_map.items():
                        aspect_w, aspect_h = map(int, ratio.split(":"))
                        for dim in dimensions:
                            width_in, height_in = map(int, dim.split("x"))
                            target_w = width_in * DPI
                            target_h = height_in * DPI

                            cropped = self.center_crop_to_aspect_ratio(img, aspect_w, aspect_h)
                            resized = cropped.resize((target_w, target_h), Image.LANCZOS)

                            out_name = f"{base_name}_{aspect_w}x{aspect_h}_{width_in}x{height_in}in.jpg"
                            out_path = os.path.join(output_dir, out_name)

                            resized.save(out_path, dpi=(DPI, DPI), quality=JPEG_QUALITY, optimize=True, subsampling=0)
                            self.log(f"Saved: {out_name} ({target_w}x{target_h}px)")

            except Exception as e:
                self.log(f"Failed to process {filename}: {str(e)}")

        self.log("\nProcessing complete. Check output folder.")

    def process_single_image(self):
        img_path = self.input_file.get()
        output_dir = self.output_folder.get()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            with Image.open(img_path) as img:
                base_name = os.path.splitext(os.path.basename(img_path))[0]

                if img.mode != 'RGB':
                    img = img.convert('RGB')

                if self.manual_crop_mode:
                    self.show_crop_window(img)

                for ratio, dimensions in self.dimensions_map.items():
                    aspect_w, aspect_h = map(int, ratio.split(":"))
                    for dim in dimensions:
                        width_in, height_in = map(int, dim.split("x"))
                        target_w = width_in * DPI
                        target_h = height_in * DPI

                        cropped = self.center_crop_to_aspect_ratio(img, aspect_w, aspect_h)
                        resized = cropped.resize((target_w, target_h), Image.LANCZOS)

                        out_name = f"{base_name}_{aspect_w}x{aspect_h}_{width_in}x{height_in}in.jpg"
                        out_path = os.path.join(output_dir, out_name)

                        resized.save(out_path, dpi=(DPI, DPI), quality=JPEG_QUALITY, optimize=True, subsampling=0)
                        self.log(f"Saved: {out_name} ({target_w}x{target_h}px)")

            self.log("\nProcessing complete. Check output folder.")

        except Exception as e:
            self.log(f"Failed to process {img_path}: {str(e)}")
    def clear_ratio_dimensions(self):
        self.dimensions_map.clear()
        self.dimensions_display.delete(0, tk.END)

    def show_crop_window(self, img):
        self.crop_window = tk.Toplevel(self)
        self.crop_window.title("Select Crop Center")
        
        orig_w, orig_h = img.size
        max_size = 500
        ratio = min(max_size / orig_w, max_size / orig_h)
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
        
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_resized)
        
        self.canvas = tk.Canvas(self.crop_window, width=max_size, height=max_size)
        self.canvas.pack()
        
        x_offset = (max_size - new_w) // 2
        y_offset = (max_size - new_h) // 2
        self.canvas.create_image(x_offset, y_offset, anchor="nw", image=self.tk_img)
        
        # Store conversion parameters
        self.crop_window.orig_w = orig_w
        self.crop_window.orig_h = orig_h
        self.crop_window.new_w = new_w
        self.crop_window.new_h = new_h
        self.crop_window.x_offset = x_offset
        self.crop_window.y_offset = y_offset
        
        self.canvas.config(cursor="crosshair")
        
        # Coordinate display
        self.coord_label = ttk.Label(self.crop_window)
        self.coord_label.pack()
        
        self.canvas.bind("<Motion>", self.update_crop_coord_display)
        self.canvas.bind("<Button-1>", self.set_crop_center)
    def update_crop_coord_display(self, event):
        x = event.x
        y = event.y
        ow = self.crop_window.orig_w
        oh = self.crop_window.orig_h
        nw = self.crop_window.new_w
        nh = self.crop_window.new_h
        xo = self.crop_window.x_offset
        yo = self.crop_window.y_offset
        
        if (xo <= x < xo + nw) and (yo <= y < yo + nh):
            img_x = int((x - xo) * (ow / nw))
            img_y = int((y - yo) * (oh / nh))
            self.coord_label.config(text=f"Original Coordinates: X={img_x}, Y={img_y}")
        else:
            self.coord_label.config(text="Move cursor over image to see coordinates")

    def set_crop_center(self, event):
        x = event.x
        y = event.y
        ow = self.crop_window.orig_w
        oh = self.crop_window.orig_h
        nw = self.crop_window.new_w
        nh = self.crop_window.new_h
        xo = self.crop_window.x_offset
        yo = self.crop_window.y_offset
        
        if (xo <= x < xo + nw) and (yo <= y < yo + nh):
            self.crop_x = int((x - xo) * (ow / nw))
            self.crop_y = int((y - yo) * (oh / nh))
            self.crop_window.destroy()
        else:
            messagebox.showerror("Invalid Selection", "Please click within the image area")

    def set_crop_center(self, event):
        self.crop_x = event.x
        self.crop_y = event.y
        self.crop_window.destroy()

    def center_crop_to_aspect_ratio(self, img, aspect_w, aspect_h):
        orig_w, orig_h = img.size
        target_ratio = aspect_w / aspect_h
        current_ratio = orig_w / orig_h

        if current_ratio > target_ratio:
            new_width = int(orig_h * target_ratio)
            left = (orig_w - new_width) // 2
            return img.crop((left, 0, left + new_width, orig_h))
        else:
            new_height = int(orig_w / target_ratio)
            top = (orig_h - new_height) // 2
            return img.crop((0, top, orig_w, top + new_height))

    def log(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

if __name__ == "__main__":
    app = ImageResizerGUI()
    app.mainloop()
