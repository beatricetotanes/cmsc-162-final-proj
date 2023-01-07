# In charge of the photos in the folder

from tkinter.ttk import Scrollbar
from tkinter import Label, Frame, messagebox
from utils import folder_path, resize_photo
from PIL import Image
from os import walk
from os.path import join
import cv2
from ResultWindow import ResultWindow


class PhotoFrame(Frame):
    def __init__(self, parent, side_frame, list_widget, done_list):
        super().__init__(
            parent,
            width=int(parent.winfo_width() * 0.7),
            height=int(parent.winfo_height() * 0.7),
            highlightthickness=2,
            highlightbackground="black")
        self.grid(column=0, row=0, sticky="nsew")
        self.grid_propagate(False)

        self.images = []
        self.dict_img = {}
        self.processed_images = []
        self.selected_image: tuple[str, int] | None = None

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
        self.done_list = done_list

        # Creates a scrollbar
        self.list_scrollbar = Scrollbar(side_frame)
        self.list_widget.config(yscrollcommand=self.list_scrollbar.set)
        self.list_scrollbar.config(command=list_widget.yview)
        self.done_list_scrollbar = Scrollbar(side_frame)
        self.done_list.config(yscrollcommand=self.done_list_scrollbar.set)
        self.done_list_scrollbar.config(command=done_list.yview)

    # Gets all the photos from the folder and creates a menu through the list box.
    # The user can choose which image to display
    def set_photos(self):
        path = folder_path()  # asks user which folder to upload
        if path == () or path == [] or path == '' and self.list_widget.size() > 0:
            return

        self.list_widget.delete(0, "end")
        self.done_list.delete(0, "end")
        self.label.grid_forget()
        self.dict_img = {}
        self.processed_images = []
        count = 0

        # All valid file types
        valid_file_types = ["jpg", "png", "gif", "jpeg", "jpg", "pcx"]

        # Finds all images in the folder
        for root, _, files in walk(path):
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
        self.done_list_scrollbar.grid(column=3, row=1, sticky="ns")

    def get_curr_image(self, get_path=False, for_removal=False):
        # Does nothing if no folder is uploaded
        if self.list_widget.size() == 0:
            return None

        img_name = ''

        # Gets currently selected image
        for idx in self.list_widget.curselection():
            img_name = self.list_widget.get(idx)
            if for_removal:
                self.selected_image = (img_name, int(idx))

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

    def show_done_photos(self, *_):
        # Does nothing if no folder is uploaded
        if self.done_list.size() == 0:
            return None

        img_idx = ''

        # Gets currently selected image
        for idx in self.done_list.curselection():
            img_idx = int(idx)

        if img_idx == '':
            return

        image = Image.fromarray(self.processed_images[img_idx][1])
        image = resize_photo(dimensions=self.resized_dimensions, img=image)
        self.label.config(image=image)
        self.label.image = image
        self.label.place(relx=0.5, rely=0.5, anchor="center")

    def remove_curr_bg(self):
        img_path = self.get_curr_image(get_path=True, for_removal=True)
        if img_path is None:
            return

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result_window = ResultWindow(self, img, self.add_applied_image)
        self.wait_window(result_window)

    def add_applied_image(self, image):
        # Gets currently selected image
        img_name, idx = self.selected_image
        image_pil = Image.fromarray(image)
        image_pil = resize_photo(dimensions=self.resized_dimensions, img=image_pil)

        self.label.config(image=image_pil)
        self.label.image = image_pil
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.processed_images.append((img_name, image))
        self.done_list.insert("end", img_name)
        self.list_widget.delete(idx)
        self.label.grid_forget()
        self.selected_image = None

    def save_all(self):
        if len(self.dict_img) == 0 and len(self.processed_images) == 0:
            return

        file_path = folder_path()

        for image in self.processed_images:
            final_img = cv2.cvtColor(image[1], cv2.COLOR_BGRA2RGBA)
            file_name = image[0].split(".")[0]
            cv2.imwrite(f"{file_path}/edited_{file_name}.png", final_img)

        messagebox.showinfo("Success", "Done saving all images!")

# References:
# https://www.geeksforgeeks.org/python-tkinter-listbox-widget/
# https://www.pythontutorial.net/tkinter/tkinter-listbox/
