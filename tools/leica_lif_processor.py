import tkinter as tk
from tkinter import filedialog, messagebox
import readlif
import numpy as np
from PIL import Image, ImageTk

class LifProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leica .lif Processor")
        self.root.configure(bg='black')
        
        self.lif_files = []
        self.lif_data = {}
        
        self.create_widgets()

    def create_widgets(self):
        # Browse button
        self.browse_button = tk.Button(self.root, text="Browse", command=self.load_files, bg='gray', fg='white')
        self.browse_button.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
        
        # Listbox for filenames
        self.file_listbox = tk.Listbox(self.root, bg='gray', fg='white', selectbackground='blue', selectforeground='white')
        self.file_listbox.grid(row=1, column=0, padx=10, pady=10, sticky='ns')
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Canvas for displaying thumbnails
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg='black')
        self.canvas.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')

        # Projection options
        self.projection_var = tk.StringVar(value="Max")
        self.projection_menu = tk.OptionMenu(self.root, self.projection_var, "Max", "Average", "Sum", "Standard Deviation", "None")
        self.projection_menu.config(bg='gray', fg='white')
        self.projection_menu.grid(row=2, column=0, padx=10, pady=10, sticky='nw')

    def load_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Leica Image Files", "*.lif")])
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.lif_files:
                    self.lif_files.append(file_path)
                    lif_file = readlif.Reader(file_path)
                    self.lif_data[file_path] = lif_file
                    self.file_listbox.insert(tk.END, file_path.split("/")[-1])
            messagebox.showinfo("Files Loaded", "Lif files loaded successfully!")

    def on_file_select(self, event):
        selected_idx = self.file_listbox.curselection()
        if selected_idx:
            file_path = self.lif_files[selected_idx[0]]
            self.display_thumbnail(file_path)

    def display_thumbnail(self, file_path):
        lif_file = self.lif_data[file_path]
        series = lif_file.get_series()[0]  # Assuming first series
        if len(series.shape) == 3:  # 3D or 3D+t
            thumbnail = self.create_projection(series)
        else:  # 2D
            thumbnail = series.get_frame()

        self.show_image(thumbnail)

    def create_projection(self, series):
        projection_type = self.projection_var.get()
        if projection_type == "Max":
            projection = np.max(series, axis=0)
        elif projection_type == "Average":
            projection = np.mean(series, axis=0)
        elif projection_type == "Sum":
            projection = np.sum(series, axis=0)
        elif projection_type == "Standard Deviation":
            projection = np.std(series, axis=0)
        else:  # None
            projection = series[0]
        return projection

    def show_image(self, image_array):
        image = Image.fromarray(image_array)
        image.thumbnail((500, 500))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = LifProcessorApp(root)
    root.mainloop()
