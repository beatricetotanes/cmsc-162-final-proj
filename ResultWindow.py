from tkinter import Toplevel, Label, Button, Scale, IntVar, filedialog, messagebox
from tkinter.colorchooser import askcolor

# from PIL.ImageGrab import grab
from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage

import cv2
from utils import remove_bg, resize_photo, swap_color, swap_bg_img


class ResultWindow(Toplevel):
    def __init__(self, parent, image, title="Resulting Image"):
        Toplevel.__init__(self, parent)
        self.title(title)
        self.parent = parent

        self.cv2_image = image
        self.__curr_image = image
        self.image_tk: None | PhotoImage = None

        self.__color: tuple | None = None
        self.__background_color: tuple | None = None

        self.image_display = Label(self,
                                   width=parent.resized_dimensions[0],
                                   height=parent.resized_dimensions[1])
        self.image_display.grid(columnspan=2, row=0)
        self.update_image(self.cv2_image)

        Button(self, command=self.get_color, text="Choose color to remove (Color Palette)").grid(column=0, row=1)
        # Button(self, command=self.get_coordinates, text="Choose color to remove (Mouse Click)").grid(column=0, row=2)
        Button(self, command=self.choose_color, text="Choose color to replace background").grid(column=0, row=2)
        Button(self, command=self.choose_image, text="Choose image to replace background").grid(column=0, row=3)
        Button(self, command=self.save_curr_img, text="Save image").grid(column=0, row=5)

        # Adjust image threshold
        Label(self, text="Change image threshold").grid(column=1, row=1)
        self.threshold_value = IntVar(self, value=15)
        self.threshold_scale = Scale(self,
                                     from_=0,
                                     to=127,
                                     variable=self.threshold_value,
                                     resolution=1,
                                     orient="horizontal",
                                     command=self.update_threshold)
        self.threshold_scale.grid(column=1, row=2)

        # Adjust saturation values
        # Lower saturation
        Label(self, text="Adjust Lower Range Saturation").grid(column=1, row=3)
        self.lower_sat_value = IntVar(self, value=0)
        self.lower_sat_scale = Scale(self,
                                     from_=0,
                                     to=255,
                                     variable=self.lower_sat_value,
                                     resolution=1,
                                     orient="horizontal",
                                     command=self.update_threshold)
        self.lower_sat_scale.grid(column=1, row=4)

        # Upper saturation
        Label(self, text="Adjust Upper Range Saturation").grid(column=1, row=5)
        self.upper_sat_value = IntVar(self, value=255)
        self.upper_sat_scale = Scale(self,
                                     from_=0,
                                     to=255,
                                     variable=self.upper_sat_value,
                                     resolution=1,
                                     orient="horizontal",
                                     command=self.update_threshold)
        self.upper_sat_scale.grid(column=1, row=6)

        # Adjust value values
        # Lower value
        Label(self, text="Adjust Lower Range Value").grid(column=1, row=7)
        self.lower_val_value = IntVar(self, value=0)
        self.lower_val_scale = Scale(self,
                                     from_=0,
                                     to=255,
                                     variable=self.lower_val_value,
                                     resolution=1,
                                     orient="horizontal",
                                     command=self.update_threshold)
        self.lower_val_scale.grid(column=1, row=8)

        # Upper value
        Label(self, text="Adjust Upper Range Value").grid(column=1, row=9)
        self.upper_val_value = IntVar(self, value=255)
        self.upper_val_scale = Scale(self,
                                     from_=0,
                                     to=255,
                                     variable=self.upper_val_value,
                                     resolution=1,
                                     orient="horizontal",
                                     command=self.update_threshold)
        self.upper_val_scale.grid(column=1, row=10)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def update_image(self, cv2_image):
        self.image_tk = resize_photo(self.parent.resized_dimensions, fromarray(cv2_image))
        self.image_display.config(image=self.image_tk)
        self.image_display.image = self.image_tk

    def update_threshold(self, _):
        if self.__color is None:
            return

        threshold = self.threshold_value.get()
        lower_sat = self.lower_sat_value.get()
        lower_val = self.lower_val_value.get()

        upper_sat = self.upper_sat_value.get()
        upper_val = self.upper_val_value.get()

        if upper_sat < lower_sat:
            self.upper_sat_value.set(lower_sat)
            upper_sat = lower_sat

        if upper_val < lower_val:
            self.upper_val_value.set(lower_val)
            upper_val = lower_val

        new_image = remove_bg(self.cv2_image,
                              self.__color,
                              threshold=threshold,
                              lower_saturation=lower_sat,
                              lower_value=lower_val,
                              upper_saturation=upper_sat,
                              upper_value=upper_val)
        self.__curr_image = new_image
        self.update_image(new_image)

    def get_color(self):
        color: tuple[tuple, str] | None = None
        while color is None or color[0] is None:
            color = askcolor(title="Choose color to isolate...")
        self.__color = color[0]

        threshold = self.threshold_value.get()
        lower_sat = self.lower_sat_value.get()
        lower_val = self.lower_val_value.get()

        upper_sat = self.upper_sat_value.get()
        upper_val = self.upper_val_value.get()

        new_image = remove_bg(self.cv2_image,
                              self.__color,
                              threshold=threshold,
                              lower_saturation=lower_sat,
                              lower_value=lower_val,
                              upper_saturation=upper_sat,
                              upper_value=upper_val)
        self.__curr_image = new_image
        self.update_image(new_image)

    def save_curr_img(self):
        file_path = filedialog.asksaveasfilename(
            initialfile="new_img",
            title="Save image...",
            filetypes=[("PNG File", "*.png"), ("Any file", "*.*")],
            defaultextension="*.png")
        print(file_path)

        bgra_img = cv2.cvtColor(self.__curr_image, cv2.COLOR_RGBA2BGRA)
        cv2.imwrite(file_path, bgra_img)

    def choose_color(self):
        color: tuple[tuple, str] | None = None
        while color is None or color[0] is None:
            color = askcolor(title="Choose color to isolate...")
        self.__background_color = color[0]

        new_img = swap_color(self.__curr_image, self.__background_color)
        self.update_image(new_img)

    def choose_image(self):
        file_path = filedialog.askopenfilename(
            initialfile="new_img",
            title="Save image...",
            filetypes=[("PNG File", "*.png"), ("Any file", "*.*")],
            defaultextension="*.png")

        new_bg = cv2.imread(file_path)
        new_bg = cv2.cvtColor(new_bg, cv2.COLOR_BGR2RGBA)

        new_img = swap_bg_img(self.__curr_image, new_bg)
        self.update_image(new_img)

    """
    def handle_mouse_click(self, event):
        image = grab()
        print(event.x, event.y)
        color = self.__curr_image[event.y][event.x]
        print(color)
        if len(color) > 3:
            color = color[:3]

        self.__color = tuple(color)

        threshold = self.threshold_value.get()
        lower_sat = self.lower_sat_value.get()
        lower_val = self.lower_val_value.get()

        upper_sat = self.upper_sat_value.get()
        upper_val = self.upper_val_value.get()

        new_image = remove_bg(self.cv2_image,
                              self.__color,
                              threshold=threshold,
                              lower_saturation=lower_sat,
                              lower_value=lower_val,
                              upper_saturation=upper_sat,
                              upper_value=upper_val)
        self.__curr_image = new_image
        self.update_image(new_image)

        self.image_display.unbind("<Button-1>")

    def get_coordinates(self):
        self.image_display.bind("<Button-1>", self.handle_mouse_click)
        messagebox.showinfo("How to use", "Please click the color you want to remove in the image screen.")

    """
