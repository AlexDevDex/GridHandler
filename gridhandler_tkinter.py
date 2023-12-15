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


root = tk.Tk()
root.title('Grid App')

window_width = 300
window_height = 200

#root.attributes('-alpha', 0.0) # makes invisible
root.attributes('-topmost', 1) #always on top
#window.lift()
#window.lift(another_window)

#window.lower()
#window.lower(another_window)

# get the user's screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

grid_size=8


# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


def cell_clicked():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    btn_image = tk.PhotoImage(file="image1.png")

@staticmethod
def make_click_through(window):
    try:
        hwnd = int(window.wm_frame(), 16)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_COLORKEY)
    except Exception as e:
        print(f"Failed to make the window click-through: {e}")

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)


root.mainloop()