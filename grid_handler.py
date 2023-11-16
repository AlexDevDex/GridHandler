import pygame
import sys
from pygame.locals import QUIT
from win32 import win32gui
import win32.lib.win32con as win32con
import pygetwindow as gw

# Initialize Pygame
pygame.init()

# Function to load and scale an image
def load_and_scale_image(image_path, scale):
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image

# Function to display images at specified coordinates
def display_images(screen, image_list):
    for image, coordinates in image_list:
        screen.blit(image, coordinates)

# Main function
def main():
    # Set up the screen with per-pixel alpha
    screen = pygame.display.set_mode((800, 600), pygame.NOFRAME | pygame.SRCALPHA)
    pygame.display.set_caption("Image Grid")

    # Load and scale images
    image1 = load_and_scale_image("image1.png", 0.2)
    image2 = load_and_scale_image("image2.png", 0.2)

    # Initial image coordinates
    image1_coordinates = (100, 100)
    image2_coordinates = (300, 300)

    # Create a list of image-coordinate pairs
    image_list = [(image1, image1_coordinates), (image2, image2_coordinates)]
    
    # Set up the window to be transparent and click-through
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_COLORKEY)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen with a transparent color
        screen.fill((0, 0, 0, 0))
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # Display images
        display_images(screen, image_list)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
