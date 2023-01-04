import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from utils import folder_path
import os

class CarouselFrame:
    def __init__(self, parent):
        self.parent = parent
        self.parent.update()
        
        self.folder = ''

        root_width = self.parent.winfo_width()
        root_height = self.parent.winfo_height()

        carousel_frame = Frame(self.parent, width=int(
           root_width*0.7), height=int(root_height*0.7), highlightthickness=2, highlightbackground="black")
        carousel_frame.grid(column=0, row=0, sticky=NSEW)

    def setPhotos(self):
        self.folder = folder_path()
        print(self.folder)