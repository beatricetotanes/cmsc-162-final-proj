import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from utils import folder_path
from photoFrame import PhotoFrame
from PIL import Image, ImageTk
import os

#  Root window
root = tk.Tk()
root.title('Programming Project') # IDE Title
root.geometry('1280x720') # Size of Window
root.update()

# Gets main window size
root_width = root.winfo_width()
root_height = root.winfo_height()

photo_frame = PhotoFrame(parent=root)

button_frame = Frame(root, width=int(
            root_width*0.7), height=int(root_height*0.14), highlightthickness=2, highlightbackground="black")
button_frame.grid(column=0, row=1, sticky=EW)

side_frame = Frame(root, width=int(
            root_width*0.2), height=int(root_height*0.7), highlightthickness=2, highlightbackground="black")
side_frame.grid(column=1, row=0)

list_label = Label(side_frame, text='Select image to view: ')
list_label.grid(column=0, row=0)
list = Listbox(side_frame, height=30, width=15)
list.grid(column=0, row=1)
list.bind('<<ListboxSelect>>', lambda event: photo_frame.showPhotos(event, list))

upload_button = Button(button_frame, text="Upload Folder",
                                command=lambda: photo_frame.setPhotos(list, side_frame=side_frame))
upload_button.grid(column=0, row=0, ipadx=10, ipady=10, padx=10)
root.mainloop()