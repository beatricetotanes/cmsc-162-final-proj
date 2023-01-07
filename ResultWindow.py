from tkinter import Toplevel, Label, Button, Scale, IntVar, filedialog, messagebox
from tkinter.colorchooser import askcolor
from tkinter.ttk import Progressbar

from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage

import cv2
from utils import remove_bg, resize_photo, swap_color, swap_bg_img


class ResultWindow(Toplevel):
    def __init__(self, parent, image, add_applied_image):
        Toplevel.__init__(self, parent)
        self.title("Result")
        self.parent = parent
        self.add_applied_image = add_applied_image

        self.cv2_image = image
        self.__initial_removal = None
        self.__curr_image = image
        self.image_tk: None | PhotoImage = None

        self.__color: tuple | None = None

        self.image_display = Label(self,
                                   width=parent.resized_dimensions[0],
                                   height=parent.resized_dimensions[1])
        self.image_display.grid(columnspan=2, row=0)
        self.update_image(self.cv2_image)

        Button(self, command=self.get_color, text="Choose color to remove (Color Palette)").grid(column=0, row=1)
        self.color_btn = Button(self, command=self.choose_color,
                                text="Choose color to replace background",
                                state="disabled")
        self.color_btn.grid(column=0, row=2)
        self.image_btn = Button(self,
                                command=self.choose_image,
                                text="Choose image to replace background",
                                state="disabled")
        self.image_btn.grid(column=0, row=3)
        Button(self, command=self.reset, text="Reset image").grid(column=0, row=4)
        Button(self, command=self.save_curr_img, text="Mark as done").grid(column=0, row=6)

        # Adjust image threshold
        Label(self, text="Change image threshold").grid(column=1, row=1)
        self.threshold_value = IntVar(self, value=15)
        self.threshold_scale = Scale(self,
                                     from_=0,
                                     to=127,
                                     variable=self.threshold_value,
                                     resolution=1,
                                     orient="horizontal",
                                     command=self.update_values,
                                     state="disabled")
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
                                     command=self.update_values,
                                     state="disabled")
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
                                     command=self.update_values,
                                     state="disabled")
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
                                     command=self.update_values,
                                     state="disabled")
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
                                     command=self.update_values,
                                     state="disabled")
        self.upper_val_scale.grid(column=1, row=10)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def update_image(self, cv2_image):
        self.image_tk = resize_photo(self.parent.resized_dimensions, fromarray(cv2_image))
        self.image_display.config(image=self.image_tk)
        self.image_display.image = self.image_tk
        if self.__color is not None:
            self.color_btn["state"] = "normal"
            self.image_btn["state"] = "normal"

    def update_values(self, _):
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

        new_image = remove_bg(self.__initial_removal,
                              self.__color,
                              threshold=threshold,
                              lower_saturation=lower_sat,
                              lower_value=lower_val,
                              upper_saturation=upper_sat,
                              upper_value=upper_val)
        self.__curr_image = new_image
        self.__initial_removal = new_image
        self.update_image(new_image)

    def get_color(self):
        color = askcolor(title="Choose color to isolate...")
        if color is None or color[0] is None:
            return
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
        self.__initial_removal = new_image
        self.color_btn["state"] = "normal"
        self.image_btn["state"] = "normal"
        self.threshold_scale["state"] = "normal"
        self.lower_sat_scale["state"] = "normal"
        self.upper_sat_scale["state"] = "normal"
        self.lower_val_scale["state"] = "normal"
        self.upper_val_scale["state"] = "normal"

    def save_curr_img(self):
        self.add_applied_image(self.__curr_image)
        self.deiconify()
        self.destroy()
        self.update()

    def choose_color(self):
        self.color_btn.grid_forget()
        bar = Progressbar(self, mode="indeterminate")
        bar.grid(column=0, row=2)
        bar.start()
        color = askcolor(title="Choose color to isolate...")
        if color is None or color[0] is None:
            bar.destroy()
            bar.update()
            self.color_btn.grid(column=0, row=2)
            return

        new_img = swap_color(self.__initial_removal, color[0])
        self.__curr_image = new_img
        self.update_image(new_img)
        bar.destroy()
        bar.update()
        self.color_btn.grid(column=0, row=2)

    def choose_image(self):
        self.image_btn.grid_forget()
        bar = Progressbar(self, mode="indeterminate")
        bar.grid(column=0, row=3)
        bar.start()
        file_path = filedialog.askopenfilename(
            initialfile="new_img",
            title="Save image...",
            filetypes=[("PNG File", "*.png"), ("JPG File", "*.jpg"), ("GIF File", "*.gif"), ("Any file", "*.*")],
            defaultextension="*.png")
        if file_path is None or file_path == () or file_path == "":
            bar.destroy()
            bar.update()
            self.image_btn.grid(column=0, row=3)
            return

        new_bg = cv2.imread(file_path)
        new_bg = cv2.cvtColor(new_bg, cv2.COLOR_BGR2RGBA)

        new_img = swap_bg_img(self.__initial_removal, new_bg)
        if new_img is None:
            messagebox.showerror("Invalid Image", "Image dimensions are too big")
        else:
            self.update_image(new_img)
            self.__curr_image = new_img
        bar.destroy()
        bar.update()
        self.image_btn.grid(column=0, row=3)

    def reset(self):
        self.update_image(self.cv2_image)
        self.__curr_image = self.cv2_image
        self.__initial_removal = None
        if self.__color is not None:
            self.color_btn["state"] = "disabled"
            self.image_btn["state"] = "disabled"
            self.threshold_scale["state"] = "disabled"
            self.lower_sat_scale["state"] = "disabled"
            self.lower_val_scale["state"] = "disabled"
            self.upper_sat_scale["state"] = "disabled"
            self.upper_val_scale["state"] = "disabled"
        self.__color = None
        self.threshold_value.set(15)
        self.lower_sat_value.set(0)
        self.lower_val_value.set(0)
        self.upper_sat_value.set(255)
        self.upper_val_value.set(255)
