import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageDisplayWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display Widget")
        self.root.configure(bg="black")  # Set the background color to black for transparency

        self.image_path = ""
        self.position_x = tk.DoubleVar(value=0.5)
        self.position_y = tk.DoubleVar(value=0.5)
        self.scale_factor = tk.DoubleVar(value=1.0)

        # Bring the window to the top and lift it periodically
        self.root.lift()
        self.root.after(1000, self.check_top)

        self.create_widgets()

    def create_widgets(self):
        # Image selection button
        select_image_button = tk.Button(self.root, text="Select Image", command=self.select_image, bg="black", fg="white", activebackground="black", activeforeground="white")
        select_image_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Scale factor entry
        scale_label = tk.Label(self.root, text="Scale Factor:", bg="black", fg="white")
        scale_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        scale_entry = tk.Entry(self.root, textvariable=self.scale_factor, width=10, bg="black", fg="white", insertbackground="white")
        scale_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        # X Position entry
        position_x_label = tk.Label(self.root, text="X Position:", bg="black", fg="white")
        position_x_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")

        position_x_entry = tk.Entry(self.root, textvariable=self.position_x, width=10, bg="black", fg="white", insertbackground="white")
        position_x_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        # Y Position entry
        position_y_label = tk.Label(self.root, text="Y Position:", bg="black", fg="white")
        position_y_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")

        position_y_entry = tk.Entry(self.root, textvariable=self.position_y, width=10, bg="black", fg="white", insertbackground="white")
        position_y_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        # Display Image button
        display_image_button = tk.Button(self.root, text="Display Image", command=self.display_image, bg="black", fg="white", activebackground="black", activeforeground="white")
        display_image_button.grid(row=4, column=0, pady=10, padx=10, sticky="w")

        # Display invis button
        display_invis_button = tk.Button(self.root, text="invisible", command=self.invisible, bg="black", fg="white", activebackground="black", activeforeground="white")
        display_invis_button.grid(row=5, column=0, pady=10, padx=10, sticky="w")

        # Exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy, bg="black", fg="white", activebackground="black", activeforeground="white")
        exit_button.grid(row=6, column=0, pady=10, padx=10, sticky="w")


        # Canvas to display the image
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="black", highlightthickness=0)
        self.canvas.grid(row=0, column=2, rowspan=5, padx=10, pady=10, sticky="e")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path = file_path

    def display_image(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        try:
            image = Image.open(self.image_path)
            image = image.resize((int(image.width * self.scale_factor.get()), int(image.height * self.scale_factor.get())))
            photo = ImageTk.PhotoImage(image)

            x = int(self.position_x.get() * self.canvas.winfo_reqwidth())
            y = int(self.position_y.get() * self.canvas.winfo_reqheight())

            # Delete previous images on the canvas
            self.canvas.delete("all")

            # Display the new image
            self.canvas.create_image(x, y, anchor=tk.NW, image=photo)
            self.canvas.image = photo  # to prevent garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying image: {str(e)}")
    
    def invisible(self):
        # Set window attributes for transparency
        #self.root.attributes('-alpha', 0.0)  # Set window transparency (0.0 is fully transparent, 1.0 is fully opaque)
        self.root.overrideredirect(True)  # Remove window decorations

        # Create a transparent canvas
        transparent_canvas = tk.Canvas(self.root, width=400, height=400, bg="black", highlightthickness=0)
        transparent_canvas.grid(row=0, column=2, rowspan=5, padx=10, pady=10, sticky="e")

        # Hide other widgets
        for widget in self.root.winfo_children():
            if widget != transparent_canvas:
                widget.grid_remove()

    def check_top(self):
    # Check if the window is still on top, and lift it if not
        if not self.root.winfo_ismapped():
            return  # If the window is not visible, no need to check

        top_level = self.root.winfo_toplevel()
        if not top_level.wm_attributes("-topmost"):
            top_level.attributes("-topmost", 1)
            top_level.lift()

        self.root.after(1000, self.check_top)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayWidget(root)

    root.mainloop()
