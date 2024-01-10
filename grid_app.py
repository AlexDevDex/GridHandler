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

def load_image_to_cell():
    print("test")
    file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if file_path:
        # Resize the image to a given size
        target_size = (80, 45)  # Adjust the size as needed
        image = Image.open(file_path)
        image = image.resize(target_size)

        # Create a PhotoImage object from the resized image
        image = ImageTk.PhotoImage(image)
        
        # Update the button's image
        #buttons[button_key].config(image=image)
        #buttons[button_key].image = image  # Keep a reference to avoid garbage collection


def on_cell_selected(button_key, variable):
    if variable.get() == 1:
        selected_cells_set.add(button_key)
    else:
            selected_cells_set.discard(button_key)
    if len(selected_cells_set)>0:
        set_image_button.config(state=tk.NORMAL)
    else:
        set_image_button.config(state=tk.DISABLED)

    print(selected_cells_set)


set_image_button = tk.Button(root, text="Set Image",compound=tk.BOTTOM, command=lambda: load_image_to_cell)
set_image_button.grid(row=0, column=1)
set_image_button.config(state=tk.DISABLED)
link_entry = tk.Entry(root)
link_entry.grid(row=0, column=0)
# password
password_label = ttk.Label(root, text="Password:")
password_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

# label frame
lf = ttk.LabelFrame(root, text='Grid Preview')
lf.grid(column=2, row=0, padx=0, pady=0, sticky=tk.NSEW)

# get the user's screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

grid_width = 4
grid_height = 4
cells = {}
selected_cells_set = set({})
buttons = {}

for row in range(grid_height):
    for column in range(grid_width):
        key = f'({row},{column})'
        cells[key] = {'row': row, 'column': column}

for key, value in cells.items():
    checkbox_variable = tk.IntVar()
    select = ttk.Checkbutton(
        lf,
        text=key,
        variable=checkbox_variable,
        onvalue=1,
        offvalue=0,
        compound=tk.RIGHT,
        command=lambda k=key, var=checkbox_variable: on_cell_selected(k, var)
    )
    select.grid(**value, ipadx=80, ipady=45, sticky=tk.NSEW)
    buttons[key] = select

# show the root window
root.mainloop()