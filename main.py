import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from utils import folder_path
from carouselFrame import CarouselFrame
import os

#  Root window
root = tk.Tk()
root.title('Programming Project') # IDE Title
root.geometry('1280x720') # Size of Window
root.update()

# Gets main window size
root_width = root.winfo_width()
root_height = root.winfo_height()



carousel_frame = CarouselFrame(parent=root)

button_style = Style()
button_style.configure('W.Tbutton', font=('calibri', 12, 'bold'))
button_frame = Frame(root, width=int(
            root_width*0.7), height=int(root_height*0.14), highlightthickness=2, highlightbackground="black")
button_frame.grid(column=0, row=1, sticky=EW)

upload_button = Button(button_frame, text="Upload Folder",
                                command=lambda: carousel_frame.setPhotos())
upload_button.grid(column=0, row=0, ipadx=10, ipady=10, padx=10)

# root.config(menu=menu_bar) # Configuring the menu bar
root.mainloop()