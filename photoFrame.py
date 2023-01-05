# In charge of the photos in the folder

import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from utils import folder_path, resize_photo
from PIL import Image
import os
import glob

class PhotoFrame:
    def __init__(self, parent):
        self.parent = parent
        self.parent.update()
        
        self.folder = ''
        self.images = []
        self.dict_img = {}

        # Gets size of root window
        self.root_width = self.parent.winfo_width()
        self.root_height = self.parent.winfo_height()

        # Photo frame
        self.photo_frame = Frame(self.parent, width=int(
           self.root_width*0.7), height=int(self.root_height*0.7), highlightthickness=2, highlightbackground="black")
        self.photo_frame.grid(column=0, row=0, sticky=NSEW)

        self.photo_frame.update()
        
        # Gets size of the photo frame
        self.photo_frame_width = self.photo_frame.winfo_width()
        self.photo_frame_height = self.photo_frame.winfo_height()

        # Initializes label that will house the photos
        self.label = Label(self.photo_frame, width=int(self.photo_frame_width*0.9), height=int(self.photo_frame_height*0.9))
        self.resized_dimen = (int(self.photo_frame_width*0.9),int(self.photo_frame_height*0.9))
    
    # Gets all the photos from the folder and creates a menu through the list box. 
    # The user can choose which image to display
    def setPhotos(self, list, side_frame):
        self.folder = folder_path() # asks user which folder to upload
        count = 0

        # Finds all images in the folder
        self.images = glob.glob(self.folder + '/*.jpg') 
        self.images+=glob.glob(self.folder + '/*.png')
        self.images+=glob.glob(self.folder + '/*.gif')
        self.images+=glob.glob(self.folder + '/*.jpeg')
        self.images+=glob.glob(self.folder + '/*.pcx')

        # Creates a dictionary with the base filename as the key and the value is the filepath for easier manipulation
        # Ex: {'img4.jpg': '/Users/juan/Documents/img4.jpg'}
        for j in self.images:
            basename = os.path.basename(j)
            list.insert(count, basename)
            count+=1
            self.dict_img[basename] = j
        
        # Creates a scrollbar
        list_vsb = Scrollbar(side_frame)
        list_vsb.grid(column=1, row=1, sticky=NS)
        list.config(yscrollcommand=list_vsb.set)
        list_vsb.config(command=list.yview)
    
    # Shows the photo selected by the user from the list
    def showPhotos(self, event, list,):

        # Does nothing if no folder is uploaded
        if list.size() == 0:
            return
            
        img_name = ''
        
        # Gets currently selected image
        for i in list.curselection():
            img_name = list.get(i)

        # Opens image
        img = Image.open(self.dict_img[img_name])

        # Resizes image
        img = resize_photo(dimensions=self.resized_dimen, img=img)

        # Displays the image
        self.label.config(image=img)
        self.label.image = img
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)


# References:
# https://www.geeksforgeeks.org/python-tkinter-listbox-widget/
# https://www.pythontutorial.net/tkinter/tkinter-listbox/
