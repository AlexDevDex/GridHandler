import pygame
import sys
import os
import re
import moviepy.editor as mp
from pygame.locals import QUIT
from win32 import win32gui
import win32.lib.win32con as win32con

from config import GRID_SIZE
from config import SCREEN_SIZE_OVERRIDE
from config import SCREEN_WIDTH
from config import SCREEN_HEIGHT

# Initialize Pygame
pygame.init()

# optional config override
if SCREEN_SIZE_OVERRIDE==False:
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h # hopefully 16:9
else:
    width, height = SCREEN_WIDTH, SCREEN_HEIGHT
#print(width, height) # 2048 1152

grid_image_width, grid_image_height = int(width/GRID_SIZE), int(height/GRID_SIZE) # the size of grid fields

# Create a 2D array to hold images in each grid field
#grid_array = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
grid_images = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
filename_pattern = re.compile(r'(\d+)-(\d+)\.(jpg|gif|png)')

def load_images_from_folder(image_folder_path):
    for filename in os.listdir(image_folder_path):
        file_path = os.path.join(image_folder_path, filename)
    
        # Check if the filename matches the pattern
    match = filename_pattern.match(filename)
    if match:
        # Extract the numbers from the filename
        row_number, col_number = map(int, match.groups()[:2])

        # Update the grid_images array with the file_path
        grid_images[row_number][col_number] = file_path
        print(grid_images)


# Function to load and scale an image (supports PNG and GIF)
def load_and_scale_image(image_path, desired_width, desired_height):
    if image_path.lower().endswith('.gif'):
        clip = mp.VideoFileClip(image_path, audio=False)
        gif_frames = [
            pygame.transform.smoothscale(pygame.image.fromstring(frame.tostring(), (frame.shape[1], frame.shape[0]), "RGB"),
                                          (desired_width, desired_height)) for
            i, frame in enumerate(clip.iter_frames(fps=clip.fps))]
        gif_duration = clip.duration
        return gif_frames, gif_duration
    else:
        image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.smoothscale(image, (desired_width, desired_height))
        return scaled_image, 0  # Return 0 duration for non-GIF images


# Function to display images at specified coordinates
def display_images(screen, image_list, current_frame):
    for image, coordinates in image_list:
        if isinstance(image, list):  # Check if it's a GIF
            screen.blit(image[current_frame], coordinates)
        else:
            screen.blit(image, coordinates)

def draw_grid(screen, width, height, field_width, field_height):
    for x in range(0, width, field_width):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, height), 1)
    for y in range(0, height, field_height):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (width, y), 1)

# Function to check for quit key combination
def check_quit_keys(): # ctrl+alt+c
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c] and keys[pygame.K_LALT] and keys[pygame.K_LCTRL]:
        pygame.quit()
        sys.exit()

# Function to toggle image show
def toggle_images(keys, show_images): # ctrl+alt+i
    if keys[pygame.K_i] and keys[pygame.K_LALT] and keys[pygame.K_LCTRL]:
        return not show_images
    return show_images

# Function to toggle image show
def toggle_grid(keys, show_grid): # ctrl+alt+i
    if keys[pygame.K_o] and keys[pygame.K_LALT] and keys[pygame.K_LCTRL]:
        return not show_grid
    return show_grid

# Main function ++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
    # Set up the screen with per-pixel alpha
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME | pygame.SRCALPHA)
    load_images_from_folder("grid_images")
    
    # Boolean variable to control image display
    show_images = True
    show_grid = False

    # Load and scale images using smoothscale
    image1, gif_duration1 = load_and_scale_image("animated1.gif", grid_image_width, grid_image_height)
    image2, gif_duration2 = load_and_scale_image("image2.jpg", grid_image_width, grid_image_height)
    image3, gif_duration3 = load_and_scale_image("image1.jpg", grid_image_width, grid_image_height)

    # Initial image coordinates
    image1_coordinates = (0, 0)
    image2_coordinates = (1024, 576)
    image3_coordinates = (0, 576)

    # Create a list of image-coordinate pairs
    image_list = [(image1, image1_coordinates), (image2, image2_coordinates),(image3, image3_coordinates)]

    # Set up the window to be transparent and click-through
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_COLORKEY)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT)

    clock = pygame.time.Clock()
    current_frame = 0
    elapsed_time = 0.0

    # --------------------- Game loop ------------------------
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        check_quit_keys()

        # Check for toggle image/grid display key combination update
        keys = pygame.key.get_pressed()
        show_images = toggle_images(keys, show_images)
        show_grid = toggle_grid(keys, show_grid)

        # Clear the screen with a transparent color
        screen.fill((0, 0, 0, 0))

        # STAY ON TOP
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        # Display images if the flag is True
        if show_images:
            display_images(screen, image_list, current_frame)
        if show_grid:
            draw_grid(screen, width, height, grid_image_width, grid_image_height)

        # Update the display
        pygame.display.flip()

        # Control GIF animation frame rate
        elapsed_time += clock.tick(30) / 1000.0
        if elapsed_time >= min(gif_duration1, gif_duration2, gif_duration3):
            elapsed_time = 0.0
            current_frame = (current_frame + 1) % len(image1)

if __name__ == "__main__":
    main()