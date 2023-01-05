import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from utils import color_palette

class ButtonFrame:

    def __init__(self, parent, photoFrame, sideFrame, list):
        self.parent = parent
        self.parent.update()

        self.photo_frame = photoFrame
        self.side_frame = sideFrame

        self.root_width = self.parent.winfo_width()
        self.root_height = self.parent.winfo_height()

        self.button_frame = Frame(self.parent, width=int(
            self.root_width*0.7), height=int(self.root_height*0.14), highlightthickness=2, highlightbackground="black")
        self.button_frame.grid(column=0, row=1, sticky=EW)

        self.upload_button = Button(self.button_frame, text="Upload Folder",
                                command=lambda: self.photo_frame.setPhotos(list, side_frame=self.side_frame))
        self.upload_button.grid(column=0, row=0, ipadx=10, ipady=10, padx=10)

        self.rm_bg = Button(self.button_frame, text='Remove Background', command=lambda: print('remove bg'))
        self.rm_bg.grid(column=1, row=0, ipadx=10, ipady=10, padx=10)

        self.trans_bg = Button(self.button_frame, text='Transparent BG', command=lambda: print('trans'))
        self.trans_bg.grid(column=2, row=0, ipadx=10, ipady=10, padx=10)

        self.color_bg = Button(self.button_frame, text='Color BG', command=lambda: color_palette())
        self.color_bg.grid(column=3, row=0, ipadx=10, ipady=10, padx=10)

        self.img_bg = Button(self.button_frame, text='Image BG', command=lambda: print('img'))
        self.img_bg.grid(column=4, row=0, ipadx=10, ipady=10, padx=10)
