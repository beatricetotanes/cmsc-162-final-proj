# -- utils.py - source code description
# This file contains general functions that are repeatedly used in the project.
# Functions: ask_filepath, folder_path
# --
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

# Opens a window to ask for the file the user wants to select and returns the filepath
def ask_filepath():
    filepath = filedialog.askopenfilename(title="Select File", filetypes=(("jpg", "*.jpg"), ("png", "*.png"), ("gif", "*.gif"), ("jpeg", "*.jpeg"), ("pcx", "*.pcx")))
    return filepath

# Opens a window to ask for the folder the user wants to choose and returns the folder path
def folder_path():
    folder = filedialog.askdirectory()
    return folder

# Resizes the photo according to the dimensions indicated
def resize_photo(dimensions, img):
    img.thumbnail(dimensions, Image.LANCZOS)
    img.resize(dimensions)
    img = ImageTk.PhotoImage(img)

    return img