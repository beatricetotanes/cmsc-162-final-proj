# -- utils.py - source code description
# This file contains general functions that are repeatedly used in the project.
# Functions: ask_filepath, folder_path
# --
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
from colorsys import rgb_to_hsv as colorsys_rgb_to_hsv


def rgb_to_hsv(values):
    # Convert to percentages
    float_rgb = values / 255

    # Convert via colorsys library
    float_hsv = colorsys_rgb_to_hsv(*float_rgb)

    # Convert to integers
    int_hsv = [int(float_hsv[0] * 180),
               int(float_hsv[1] * 255),
               int(float_hsv[2] * 255)]

    return int_hsv


# Remove the background on the image
def remove_bg(image,
              color_to_isolate,
              threshold=15,
              lower_saturation=0,
              lower_value=0,
              upper_saturation=255,
              upper_value=255):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    original = image.copy()

    if color_to_isolate is None:
        return

    # Convert RGB values to HSV
    hsv_color = rgb_to_hsv(np.asarray(color_to_isolate))

    lower = np.asarray([hsv_color[0] - threshold, lower_saturation, lower_value])
    upper = np.asarray([hsv_color[0] + threshold, upper_saturation, upper_value])
    mask = cv2.inRange(img_hsv, lower, upper)

    # negate mask
    mask = 255 - mask

    # apply morphology to remove isolated extraneous noise
    # use borderconstant of black since foreground touches the edges
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask -- blur then stretch
    # blur alpha channel
    mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=2, sigmaY=2, borderType=cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)

    # put mask into alpha channel
    result = cv2.cvtColor(original, cv2.COLOR_RGB2RGBA)
    result[:, :, 3] = mask

    return result


# Opens a window to ask for the file the user wants to select and returns the filepath
def ask_filepath():
    filepath = filedialog.askopenfilename(title="Select File", filetypes=(("jpg", "*.jpg"),
                                                                          ("png", "*.png"),
                                                                          ("gif", "*.gif"),
                                                                          ("jpeg", "*.jpeg"),
                                                                          ("pcx", "*.pcx")))
    return filepath


# Opens a window to ask for the folder the user wants to choose and returns the folder path
def folder_path():
    return filedialog.askdirectory()


# Resizes the photo according to the dimensions indicated
def resize_photo(dimensions, img):
    img.thumbnail(dimensions, Image.LANCZOS)
    img.resize(dimensions)
    return ImageTk.PhotoImage(img)


def swap_color(original, color):
    image = original.copy()
    indices = np.argwhere(image == 0)
    new_color = np.array([*color, 255])
    image[indices[:, 0], indices[:, 1]] = new_color
    return image


def swap_bg_img(original, bg):
    try:
        image = original.copy()
        indices = np.argwhere(image == 0)
        image[indices[:, 0], indices[:, 1]] = bg[indices[:, 0], indices[:, 1]]
    except IndexError:
        return None

    return image
