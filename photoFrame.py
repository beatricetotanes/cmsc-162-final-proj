import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from utils import folder_path, resize_photo
from PIL import Image, ImageTk
import os
import glob

class PhotoFrame:
    def __init__(self, parent):
        self.parent = parent
        self.parent.update()
        
        self.folder = ''
        self.images = []
        self.dict_img = {}

        self.root_width = self.parent.winfo_width()
        self.root_height = self.parent.winfo_height()

        self.photo_frame = Frame(self.parent, width=int(
           self.root_width*0.7), height=int(self.root_height*0.7), highlightthickness=2, highlightbackground="black")
        self.photo_frame.grid(column=0, row=0, sticky=NSEW)

        self.photo_frame.update()
        
        self.photo_frame_width = self.photo_frame.winfo_width()
        self.photo_frame_height = self.photo_frame.winfo_height()
        self.label = Label(self.photo_frame, width=int(self.photo_frame_width*0.9), height=int(self.photo_frame_height*0.9))
        self.resized_dimens = (int(self.photo_frame_width*0.9),int(self.photo_frame_height*0.9))

    def setPhotos(self, list, side_frame):
        self.folder = folder_path()
        count = 0

        self.images = glob.glob(self.folder + '/*.jpg') 
        self.images+=glob.glob(self.folder + '/*.png')
        self.images+=glob.glob(self.folder + '/*.gif')
        self.images+=glob.glob(self.folder + '/*.jpeg')
        self.images+=glob.glob(self.folder + '/*.pcx')

        for j in self.images:
            basename = os.path.basename(j)
            list.insert(count, basename)
            count+=1
            self.dict_img[basename] = j
        
        list_vsb = Scrollbar(side_frame)
        list_vsb.grid(column=1, row=1, sticky=NS)
        list.config(yscrollcommand=list_vsb.set)
        list_vsb.config(command=list.yview)
     
    def showPhotos(self, event, list,):
        if list.size() == 0:
            return
            
        img_name = ''
        
        for i in list.curselection():
            img_name = list.get(i)

        dimensions=(int(self.photo_frame_width*0.9),int(self.photo_frame_height*0.9))

        img = Image.open(self.dict_img[img_name])

        # Resize image
        img = resize_photo(dimensions=self.resized_dimens, img=img)

        self.label.config(image=img)
        self.label.image = img
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)




        

