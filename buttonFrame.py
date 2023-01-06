# Houses all the buttons

from tkinter import Frame, Button
from tkinter import colorchooser
from utils import ask_filepath


class ButtonFrame(Frame):

    def __init__(self, parent, set_photos, remove_bg):
        super().__init__(
            parent,
            highlightthickness=1,
            highlightbackground="black"
        )
        parent.update_idletasks()

        # For uploading whole folders w/ images
        self.upload_button = Button(self,
                                    text="Upload Folder",
                                    command=set_photos)
        self.upload_button.grid(column=0, row=0, ipadx=10, ipady=10, padx=10)

        # For removal of background of all images
        self.rm_bg = Button(self, text='Remove Background', command=remove_bg)
        self.rm_bg.grid(column=1, row=0, ipadx=10, ipady=10, padx=10)
    # Reference: https://www.geeksforgeeks.org/python-tkinter-choose-color-dialog/
