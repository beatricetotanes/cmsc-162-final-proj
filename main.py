import tkinter as tk
from tkinter import Frame, Label, Listbox
from photoFrame import PhotoFrame
from buttonFrame import ButtonFrame

#  Root window
root = tk.Tk()
root.title('Programming Project')  # IDE Title
root.geometry('1280x720')  # Size of Window
root.update()

# Gets main window size
root_width = root.winfo_width()
root_height = root.winfo_height()
root.rowconfigure(0, weight=2)

# Initializes the Side Frame
side_frame = Frame(root,
                   width=int(root_width * 0.5),
                   highlightthickness=2,
                   highlightbackground="black")
side_frame.grid(column=1, row=0, rowspan=2, sticky="nse")

# Initializes the list selection for the images
list_label = Label(side_frame, text='Select image to view: ')
list_label.grid(column=0, row=0)
list_widget = Listbox(side_frame, height=30, width=20)
list_widget.grid(column=0, row=1)

Label(side_frame, text="Processed images").grid(column=2, row=0)
done_list = Listbox(side_frame, height=30, width=20)
done_list.grid(column=2, row=1)

# Initializes the Photo Frame
photo_frame = PhotoFrame(root, side_frame, list_widget, done_list)

list_widget.bind('<<ListboxSelect>>', photo_frame.show_photos)
done_list.bind('<<ListboxSelect>>', photo_frame.show_done_photos)

# Initializes the button frame for the buttons
button_frame = ButtonFrame(root, photo_frame.set_photos, photo_frame.remove_curr_bg, photo_frame.save_all)
button_frame.grid(column=0, row=1, sticky="ew")

root.mainloop()
