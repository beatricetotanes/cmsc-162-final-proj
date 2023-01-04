import tkinter as tk
from tkinter import *

#  Root window
root = tk.Tk()
root.title('Programming Project') # IDE Title
root.geometry('1280x720') # Size of Window

# Gets main window size
root_width = root.winfo_width()
root_height = root.winfo_height()

root.update()

# root.config(menu=menu_bar) # Configuring the menu bar
root.mainloop()