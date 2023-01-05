# Houses all the buttons

import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from tkinter import colorchooser
from utils import ask_filepath

class ButtonFrame:

    def __init__(self, parent, photoFrame, sideFrame, list):
        self.parent = parent
        self.parent.update()

        self.photo_frame = photoFrame
        self.side_frame = sideFrame

        # Gets size of root window
        self.root_width = self.parent.winfo_width()
        self.root_height = self.parent.winfo_height()

        # Button frame
        self.button_frame = Frame(self.parent, width=int(
            self.root_width*0.7), height=int(self.root_height*0.14), highlightthickness=1, highlightbackground="black")
        self.button_frame.grid(column=0, row=1, sticky=EW)

        # For uploading whole folders w/ images
        self.upload_button = Button(self.button_frame, text="Upload Folder",
                                command=lambda: self.photo_frame.setPhotos(list, side_frame=self.side_frame))
        self.upload_button.grid(column=0, row=0, ipadx=10, ipady=10, padx=10)

        # For removal of background of all images
        self.rm_bg = Button(self.button_frame, text='Remove Background', command=lambda: print('remove bg'))
        self.rm_bg.grid(column=1, row=0, ipadx=10, ipady=10, padx=10)

        # Replacing the background with a transparent one
        self.trans_bg = Button(self.button_frame, text='Transparent Background', command=lambda: print('trans'))
        self.trans_bg.grid(column=2, row=0, ipadx=10, ipady=10, padx=10)

        # Let's user choose a color and replaces the background of image with that color
        self.color_bg = Button(self.button_frame, text='Color Background', command=lambda: self.color_palette())
        self.color_bg.grid(column=3, row=0, ipadx=10, ipady=10, padx=10)

        # Let's user choose an image and replaces the background of image with that other image
        self.img_bg = Button(self.button_frame, text='Image Background', command=lambda: self.setImageBG())
        self.img_bg.grid(column=4, row=0, ipadx=10, ipady=10, padx=10)

    # Ask user what image to make as a background
    # DREW: Add code to replace bg w/ chosen image
    def setImageBG(self):
        filepath = ask_filepath()
        print(filepath)

    # Asks user what color he/she wants as a background
    # DREW: Add code to replace bg w/ chosen color
    def color_palette(self):
        color = colorchooser.askcolor(title='Choose color')
        return color # returns rgb tuple
