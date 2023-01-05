import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from utils import folder_path
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
        self.text_lbl = StringVar()
        self.text_lbl.set("test")

        self.root_width = self.parent.winfo_width()
        self.root_height = self.parent.winfo_height()

        self.photo_frame = Frame(self.parent, width=int(
           self.root_width*0.7), height=int(self.root_height*0.7), highlightthickness=2, highlightbackground="black")
        self.photo_frame.grid(column=0, row=0, sticky=NSEW)

        self.photo_frame.update()

        self.photo_frame_width = self.photo_frame.winfo_width()
        self.photo_frame_height = self.photo_frame.winfo_height()

        

        # self.textbox = Text(photo_frame)
        # self.textbox.grid(column=0, row=0)

    def setPhotos(self):
        self.folder = folder_path()
        file_directory = os.listdir(self.folder)
        widths = []
        heights = []
        
        self.images = glob.glob(self.folder + '/*.jpg')
        img = ImageTk.PhotoImage(file = '10067.jpeg')
        print(img)
        self.textbox.image_create(tk.END, image=img)
        
        # print(images)\

    def testPhotos(self, list):
        self.folder = folder_path()
        count = 0

        self.images = glob.glob(self.folder + ('/*.jpg')) 
        for j in self.images:
            basename = os.path.basename(j)
            list.insert(count, basename)
            count+=1
            self.dict_img[basename] = j

        print(self.dict_img)
     
    def showPhotos1(self, event, list):
        img_name = ''

        tmp = StringVar()
        tmp.set('test')
        
        for i in list.curselection():
            img_name = list.get(i)

        # dimensions = (self.photo_frame.winfo_reqwidth(), self.photo_frame.winfo_reqheight())
        dimensions=(self.photo_frame_width,self.photo_frame_height)
        print(dimensions)

        img = Image.open(self.dict_img[img_name])
        print(img)
        # Resize image
        img.thumbnail(dimensions, Image.LANCZOS)
        img.resize(dimensions)
        # image_tk = PhotoImage(img)
        test = ImageTk.PhotoImage(img)
        print(test)

        self.label = Label(self.photo_frame, image=test, width=int(self.photo_frame_width), height=int(self.photo_frame_height))
        self.label.image = test
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)
        # self.label.configure(image=img)
        # label.grid(column=0, row=0)

        # print(list.curselection())


        

