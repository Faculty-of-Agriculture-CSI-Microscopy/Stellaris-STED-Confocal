import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk
from aicsimageio.writers import OmeTiffWriter
from readlif.reader import LifFile
import os

class LifProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leica .lif Processor")
        self.root.geometry("1200x800")  # Increased height for better visibility
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.apply_style()

        self.lif_files = []
        self.lif_data = {}
        self.output_folder = None

        self.create_widgets()

    def apply_style(self):
        self.style.configure('TButton', font=('Helvetica', 12), padding=6, background='#6200EE', foreground='white')
        self.style.configure('TCheckbutton', font=('Helvetica', 12), background='#F5F5F5', foreground='black')
        self.style.configure('TLabel', font=('Helvetica', 12), background='#F5F5F5', foreground='black')
        self.style.configure('TListbox', font=('Helvetica', 12), background='#F5F5F5', foreground='black')
        self.style.configure('TFrame', background='#F5F5F5')
        self.style.configure('TCanvas', background='#F5F5F5')

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Browse button
        self.browse_button = ttk.Button(main_frame, text="Browse", command=self.load_files)
        self.browse_button.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Listbox for filenames with scrollbar
        self.file_frame = ttk.Frame(main_frame)
        self.file_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ns')
        self.file_scrollbar = ttk.Scrollbar(self.file_frame)
        self.file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox = tk.Listbox(self.file_frame, selectmode=tk.SINGLE, yscrollcommand=self.file_scrollbar.set, bg='#F5F5F5', font=('Helvetica', 12))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_scrollbar.config(command=self.file_listbox.yview)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)

        # Canvas for displaying thumbnails with scrollbar
        self.canvas_frame = ttk.Frame(main_frame)
        self.canvas_frame.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky='nsew')
        self.canvas_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.canvas_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=600, bg='white', xscrollcommand=self.canvas_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_scrollbar.config(command=self.canvas.xview)

        # Projection options
        self.projection_var = tk.StringVar(value="Max")
        projection_label = ttk.Label(main_frame, text="Projection Type")
        projection_label.grid(row=2, column=0, padx=10, pady=10, sticky='nw')
        self.projection_menu = tk.Listbox(main_frame, listvariable=self.projection_var, selectmode=tk.MULTIPLE, bg='#F5F5F5', font=('Helvetica', 12))
        for item in ["Max", "Average", "Sum", "Standard Deviation", "None"]:
            if item not in self.projection_menu.get(0, tk.END):
                self.projection_menu.insert(tk.END, item)
        self.projection_menu.grid(row=3, column=0, padx=10, pady=10, sticky='nw')

        # Batch conversion button
        self.batch_convert_button = ttk.Button(main_frame, text="Batch Convert", command=self.batch_convert)
        self.batch_convert_button.grid(row=7, column=0, padx=10, pady=10, sticky='nw')

        # Process files button
        self.process_files_button = ttk.Button(main_frame, text="Process Files", command=self.process_files)
        self.process_files_button.grid(row=8, column=0, padx=10, pady=10, sticky='nw')

        # Additional settings (checkboxes)
        self.original_folder_var = tk.BooleanVar(value=True)
        self.original_folder_checkbox = ttk.Checkbutton(main_frame, text="Save to Original Folder", variable=self.original_folder_var)
        self.original_folder_checkbox.grid(row=9, column=0, padx=10, pady=5, sticky='nw')

        self.specify_folder_button = ttk.Button(main_frame, text="Specify Folder", command=self.specify_folder)
        self.specify_folder_button.grid(row=10, column=0, padx=10, pady=5, sticky='nw')

    def specify_folder(self):
        self.output_folder = filedialog.askdirectory()
        if not self.output_folder:
            self.output_folder = None

    def load_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Leica Image Files", "*.lif")])
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.lif_files:
                    self.lif_files.append(file_path)
                    dataset = self.read_lif_file(file_path)
                    if dataset is not None:
                        self.lif_data[file_path] = dataset
                        self.file_listbox.insert(tk.END, os.path.basename(file_path))
                    else:
                        messagebox.showerror("Error", f"Failed to load file:\n{file_path}")
            messagebox.showinfo("Files Loaded", "Lif files loaded successfully!")

    def read_lif_file(self, file_path):
        try:
            lif_file = LifFile(file_path)
            images = []
            for image in lif_file.get_iter_image():
                frames = [np.array(frame) for frame in image.get_iter_t()]
                metadata = {
                    'Z': image.dims[2],
                    'T': image.dims[3],
                    'M': image.dims[9] if 9 in image.dims else 1,
                    'Size': sum(frame.nbytes for frame in frames) / 1e6  # Approximate size in MB
                }
                images.append((frames, metadata))
            return images
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def on_file_select(self, event):
        selected_idx = self.file_listbox.curselection()
        if selected_idx:
            file_path = self.lif_files[selected_idx[0]]
            self.display_file_details(file_path)

    def display_file_details(self, file_path):
        dataset = self.lif_data.get(file_path)
        if dataset is None:
            messagebox.showerror("Error", f"Failed to load dataset for file: {file_path}")
            return

        try:
            self.canvas.delete("all")
            y_offset = 10
            for i, (frames, metadata) in enumerate(dataset):
                checkbox = tk.Checkbutton(self.canvas, text=f"Image {i+1}", anchor='w', bg='white')
                self.canvas.create_window(10, y_offset, anchor='nw', window=checkbox)
                y_offset += 30
                self.canvas.create_text(10, y_offset, anchor='nw', text=f"Z-slices: {metadata['Z']}, Time points: {metadata['T']}, Tiles: {metadata['M']}, Size: {metadata['Size']:.2f} MB", fill='black')
                y_offset += 30
                thumbnail = self.create_projection(frames) if metadata['Z'] > 1 else frames[0]

                self.show_image(thumbnail, y_offset)
                y_offset += 150
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file {file_path}: {e}")

    def create_projection(self, frames):
        selected_projections = self.projection_menu.curselection()
        projection_types = [self.projection_menu.get(i) for i in selected_projections]
        projections = {}
        frames_array = np.stack(frames, axis=0)  # Stack frames into a single NumPy array
        for projection_type in projection_types:
            if projection_type == "Max":
                projections["Max"] = np.max(frames_array, axis=0)
            elif projection_type == "Average":
                projections["Average"] = np.mean(frames_array, axis=0)
            elif projection_type == "Sum":
                projections["Sum"] = np.sum(frames_array, axis=0)
            elif projection_type == "Standard Deviation":
                projections["Standard Deviation"] = np.std(frames_array, axis=0)
            elif projection_type == "None":
                projections["None"] = frames_array[0]
        return projections

    def show_image(self, image_array, y_offset):
        if isinstance(image_array, dict):
            image_array = image_array[list(image_array.keys())[0]]  # Get the first projection
        if image_array.ndim == 3:
            image_array = image_array[:, :, 0]
        image = Image.fromarray(self.convert_image(image_array))
        image.thumbnail((200, 200))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(10, y_offset, anchor="nw", image=self.tk_image)

    def convert_image(self, array):
        if array.dtype == np.uint8:
            return array
        elif array.dtype == np.uint16:
            array = (array / 256).astype(np.uint8)
            return array
        else:
            array = (array / np.max(array) * 255).astype(np.uint8)
            return array

    def process_files(self):
        print("Processing files...")
        selected_files = [file for i, file in enumerate(self.lif_files) if self.file_listbox.selection_includes(i)]
        if not selected_files:
            messagebox.showerror("Error", "No files selected.")
            return
        
        for file_path in selected_files:
            dataset = self.lif_data.get(file_path)
            if dataset is None:
                print(f"No dataset found for {file_path}")
                continue

            output_folder = self.output_folder if not self.original_folder_var.get() else os.path.dirname(file_path)

            for i, (frames, _) in enumerate(dataset):
                projections = self.create_projection(frames)
                for projection_type, projection_data in projections.items():
                    output_path = os.path.join(output_folder, f"{os.path.basename(file_path).split('.')[0]}_{i}_{projection_type}.tiff")
                    print(f"Saving {output_path}")
                    OmeTiffWriter.save(projection_data, output_path, dim_order='YX')

        messagebox.showinfo("Processing Complete", "File processing complete.")

    def batch_convert(self):
        print("Batch converting files...")
        selected_files = [file for i, file in enumerate(self.lif_files) if self.file_listbox.selection_includes(i)]
        if not selected_files:
            messagebox.showerror("Error", "No files selected.")
            return
        
        for file_path in selected_files:
            dataset = self.lif_data.get(file_path)
            if dataset is None:
                print(f"No dataset found for {file_path}")
                continue

            output_folder = self.output_folder if not self.original_folder_var.get() else os.path.dirname(file_path)

            for i, (frames, _) in enumerate(dataset):
                projections = self.create_projection(frames)
                for projection_type, projection_data in projections.items():
                    output_path = os.path.join(output_folder, f"{os.path.basename(file_path).split('.')[0]}_{i}_{projection_type}.tiff")
                    print(f"Saving {output_path}")
                    OmeTiffWriter.save(projection_data, output_path, dim_order='YX')

        messagebox.showinfo("Conversion Complete", "Batch conversion complete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LifProcessorApp(root)
    root.mainloop()
