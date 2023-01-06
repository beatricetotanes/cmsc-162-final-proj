# In charge of the photos in the folder

from tkinter.ttk import Scrollbar
from tkinter import Label, Frame
from utils import folder_path, resize_photo
from PIL import Image
from os import walk
from os.path import join
import cv2
from ResultWindow import ResultWindow


class PhotoFrame(Frame):
    def __init__(self, parent, side_frame, list_widget):
        super().__init__(
            parent,
            width=int(parent.winfo_width() * 0.7),
            height=int(parent.winfo_height() * 0.7),
            highlightthickness=2,
            highlightbackground="black")
        self.grid(column=0, row=0, sticky="nsew")
        self.grid_propagate(False)

        self.folder: str | None = None
        self.images = []
        self.dict_img = {}

        # Gets size of the photo frame
        self.update_idletasks()
        parent.update_idletasks()
        self.photo_frame_width = self.winfo_reqwidth()
        self.photo_frame_height = self.winfo_reqheight()

        # Initializes label that will house the photos
        self.label = Label(self,
                           width=int(self.photo_frame_width * 0.9),
                           height=int(self.photo_frame_height * 0.9))
        self.resized_dimensions = int(self.photo_frame_width * 0.9), int(self.photo_frame_height * 0.9)

        # Instance of the list_widget
        self.list_widget = list_widget

        # Creates a scrollbar
        self.list_scrollbar = Scrollbar(side_frame)
        self.list_widget.config(yscrollcommand=self.list_scrollbar.set)
        self.list_scrollbar.config(command=list_widget.yview)

    # Gets all the photos from the folder and creates a menu through the list box.
    # The user can choose which image to display
    def set_photos(self):
        self.folder = folder_path()  # asks user which folder to upload

        self.list_widget.delete(0, "end")
        self.label.grid_forget()
        count = 0

        # All valid file types
        valid_file_types = ["jpg", "png", "gif", "jpeg", "jpg", "pcx"]

        # Finds all images in the folder
        for root, _, files in walk(self.folder):
            for file in files:
                file_type = file.split(".")[-1]
                if file_type in valid_file_types:
                    self.images.append(file)
                    self.list_widget.insert(count, file)

                    # Creates a key-value pair with the base filename as the key and
                    # the value is the filepath for easier manipulation
                    # Ex: {'img4.jpg': '/Users/juan/Documents/img4.jpg'}
                    self.dict_img[file] = join(root, file)
                    count += 1

        self.list_scrollbar.grid(column=1, row=1, sticky="ns")

    def get_curr_image(self, get_path=False):
        # Does nothing if no folder is uploaded
        if self.list_widget.size() == 0:
            return None

        img_name = ''

        # Gets currently selected image
        for image in self.list_widget.curselection():
            img_name = self.list_widget.get(image)

        if img_name is None or img_name == '':
            return

        path = self.dict_img[img_name]

        return path if get_path else img_name

    # Shows the photo selected by the user from the list
    def show_photos(self, *_):

        img_path = self.get_curr_image(get_path=True)
        if img_path is None:
            return

        # Opens image
        img = Image.open(img_path)

        # Resizes image
        img = resize_photo(dimensions=self.resized_dimensions, img=img)

        # Displays the image
        self.label.config(image=img)
        self.label.image = img
        self.label.place(relx=0.5, rely=0.5, anchor="center")

    def remove_curr_bg(self):
        img_path = self.get_curr_image(get_path=True)
        if img_path is None:
            return

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        ResultWindow(self, img)

# References:
# https://www.geeksforgeeks.org/python-tkinter-listbox-widget/
# https://www.pythontutorial.net/tkinter/tkinter-listbox/
