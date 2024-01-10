import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageGrid:
    def __init__(self, master, rows, cols):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.images = [[None for _ in range(cols)] for _ in range(rows)]
        self.selected_cells = set()

        # Create the grid of selectable cells
        for row in range(rows):
            for col in range(cols):
                cell = tk.Canvas(master, width=50, height=50, highlightthickness=1, highlightbackground="black")
                cell.grid(row=row, column=col)
                cell.bind("<Button-1>", lambda event, row=row, col=col: self.toggle_cell_selection(row, col))
                self.images[row][col] = cell
                print(f"Created cell at ({row}, {col}): {cell}")

        # Create the buttons on the left side
        self.set_image_button = tk.Button(master, text="Set Image", command=self.set_image)
        self.set_image_button.grid(row=0, column=cols+1)

        self.delete_image_button = tk.Button(master, text="Delete Image", command=self.delete_image)
        self.delete_image_button.grid(row=1, column=cols+1)

        self.load_grid_button = tk.Button(master, text="Load Grid", command=self.load_grid)
        self.load_grid_button.grid(row=2, column=cols+1)

        self.link_entry = tk.Entry(master)
        self.link_entry.grid(row=3, column=cols+1)

    def toggle_cell_selection(self, row, col):
        if (row, col) in self.selected_cells:
            self.selected_cells.remove((row, col))
            self.images[row][col].config(highlightbackground="black")
        else:
            self.selected_cells.add((row, col))
            self.images[row][col].config(highlightbackground="red")

    def select_cell(self, row, col):
        if (row, col) in self.selected_cells:
            self.selected_cells.remove((row, col))
            self.images[row][col].delete("all")
        else:
            self.selected_cells.add((row, col))

    def set_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            img = Image.open(file_path)
            photo = ImageTk.PhotoImage(img)
            self.master.photo = photo
            self.master.img = img
            self.master.filename = file_path

            if self.link_entry.get().startswith("https://i.imgur.com/") and len(self.selected_cells) > 0:
                x1, y1, x2, y2 = self.get_selected_cells_bbox()
                img = img.crop((x1, y1, x2, y2))
                img.thumbnail((50, 50))
                photo = ImageTk.PhotoImage(img)

                for row, col in self.selected_cells:
                    if self.images[row][col]:
                        self.images[row][col].delete("all")
                    self.images[row][col] = tk.Canvas(self.master, width=50, height=50, highlightthickness=1, highlightbackground="black")
                    self.images[row][col].create_image(0, 0, anchor="nw", image=photo)
                    self.images[row][col].grid(row=row, column=col)

    def delete_image(self):
        for row, col in self.selected_cells:
            if self.images[row][col]:
                self.images[row][col].delete("all")
                self.images[row][col] = None
        self.selected_cells.clear()

    def load_grid(self):
        if self.master.filename:
            img = Image.open(self.master.filename)
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.images[row][col]:
                        x1, y1, x2, y2 = self.get_selected_cells_bbox()
                        img_crop = img.crop((x1, y1, x2, y2))
                        img_crop.thumbnail((50, 50))
                        photo = ImageTk.PhotoImage(img_crop)
                        self.images[row][col].create_image(0, 0, anchor="nw", image=photo)

    def get_selected_cells_bbox(self):
        rows, cols = zip(*self.selected_cells)
        x1, y1 = min(cols), min(rows)
        x2, y2 = max(cols)+1, max(rows)+1
        return x1*50, y1*50, x2*50, y2*50

root = tk.Tk()
root.title("Image Grid")
app = ImageGrid(root, 4, 4)
root.mainloop()
