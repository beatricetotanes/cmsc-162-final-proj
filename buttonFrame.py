import tkinter as tk
from tkinter.ttk import *
from tkinter import *

class ButtonFrame:

    def __init__(self, parent):
        self.parent = parent
        self.parent.update()

        self.root_width = self.parent.winfo_width()
        self.root_height = self.parent.winfo_height()

        button_frame = Frame(self.parent, width=int(
            self.root_width*0.7), height=int(self.root_height*0.14), highlightthickness=2, highlightbackground="black")
        button_frame.grid(column=0, row=1, sticky=EW)

        upload_button = Button(button_frame, text="Upload Folder",
                                command=lambda: photo_frame.setPhotos(list, side_frame=side_frame))
upload_button.grid(column=0, row=0, ipadx=10, ipady=10, padx=10)