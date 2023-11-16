import pygame
import sys
import imageio
import moviepy.editor as mp
from pygame.locals import QUIT
from win32 import win32gui
import win32.lib.win32con as win32con
import pygetwindow as gw

# Initialize Pygame
pygame.init()

# Function to load and scale an image (supports PNG and GIF)
def load_and_scale_image(image_path, scale):
    if image_path.lower().endswith('.gif'):
        clip = mp.VideoFileClip(image_path, audio=False)
        gif_frames = [pygame.transform.smoothscale(pygame.image.fromstring(frame.tostring(), (frame.shape[1], frame.shape[0]), "RGB"), (int(frame.shape[1] * scale), int(frame.shape[0] * scale))) for i, frame in enumerate(clip.iter_frames(fps=clip.fps))]
        gif_duration = clip.duration
        return gif_frames, gif_duration
    else:
        image = pygame.image.load(image_path).convert_alpha()
        original_size = image.get_size()
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        scaled_image = pygame.transform.smoothscale(image, new_size)
        return scaled_image, 0  # Return 0 duration for non-GIF images

# Function to display images at specified coordinates
def display_images(screen, image_list, current_frame):
    for image, coordinates in image_list:
        if isinstance(image, list):  # Check if it's a GIF
            screen.blit(image[current_frame], coordinates)
        else:
            screen.blit(image, coordinates)

# Main function
def main():
    # Set up the screen with per-pixel alpha
    screen = pygame.display.set_mode((800, 600), pygame.NOFRAME | pygame.SRCALPHA)
    pygame.display.set_caption("Image Grid")

    # Load and scale images using smoothscale
    image1, gif_duration1 = load_and_scale_image("animated1.gif", 0.1)
    image2, gif_duration2 = load_and_scale_image("image2.jpg", 0.1)

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
    clock = pygame.time.Clock()
    current_frame = 0
    elapsed_time = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen with a transparent color
        screen.fill((0, 0, 0, 0))

        # WE STAY ON TOP
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        # Display images
        display_images(screen, image_list, current_frame)

        # Update the display
        pygame.display.flip()

        # Control GIF animation frame rate
        elapsed_time += clock.tick(30) / 1000.0
        if elapsed_time >= min(gif_duration1, gif_duration2):
            elapsed_time = 0.0
            current_frame = (current_frame + 1) % len(image1)

if __name__ == "__main__":
    main()