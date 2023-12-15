import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import win32gui
import win32.lib.win32con as win32con
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# root window
root = tk.Tk()
root.title('Grid App')

def on_cell_click(button_key):
    file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if file_path:
        # Resize the image to a given size
        target_size = (50, 50)  # Adjust the size as needed
        image = Image.open(file_path)
        image = image.resize(target_size)

        # Create a PhotoImage object from the resized image
        image = ImageTk.PhotoImage(image)

        # Update the button's image
        buttons[button_key].config(image=image)
        buttons[button_key].image = image  # Keep a reference to avoid garbage collection

username_label = ttk.Label(root, text="Username:")
username_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
# password
password_label = ttk.Label(root, text="Password:")
password_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

# label frame
lf = ttk.LabelFrame(root, text='Grid Preview')
lf.grid(column=1, row=0, padx=0, pady=0, sticky=tk.NSEW)

# get the user's screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

grid_width = 2
grid_height = 4
cells = {}

buttons = {}  # Store references to the buttons

for row in range(grid_height):
    for column in range(grid_width):
        key = f'({row},{column})'
        cells[key] = {'row': row, 'column': column}

for key, value in cells.items():
    # Create a cell button
    button = ttk.Button(
        lf,
        text=key,
        width=50,
        command=lambda k=key: on_cell_click(k)  # Pass the key to the function
    )
    button.grid(**value, padx=50, pady=50, sticky=tk.NSEW)
    buttons[key] = button  # Store a reference to the button

# show the root window
root.mainloop()