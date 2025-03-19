import customtkinter as ctk
from PIL import Image
from io import BytesIO
import sqlite3
import textwrap
from tkinter.font import Font


def change_picture_to_size(picture):
    # return 600, (picture.size[1] + (600 - picture.size[0]))
    ratio = 600 / float(picture.size[0])
    height = int((float(picture.size[1]) * float(ratio)))
    return 600, height


def wrap_label_text_in_frame(frame, label, column_index):
    frame.update_idletasks()
    max_width_pixels = (frame.winfo_width()-frame.grid_bbox(column_index, 0, column_index, frame.grid_size()[1] - 1)[2]
                        - 80)

    font = Font(font=label.cget("font"))
    average_char_width = font.measure("0")
    max_width_chars = max_width_pixels // average_char_width

    text = label.cget("text")
    wrapped_text = "\n".join([textwrap.fill(line, width=max_width_chars) for line in text.split('\n')])
    label.configure(text=wrapped_text)
    return label


class CatalogDesign1:
    def __init__(self, background_frame):
        self.background_frame = background_frame
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM Catalog")
        self.rows = self.cursor.fetchall()
        self.create_frames()

    def create_product_frame(self, i):
        frame = ctk.CTkFrame(self.background_frame)
        frame.pack(fill="both", expand=True, pady=10)
        frame.columnconfigure((0, 3), weight=1)

        image_data = self.rows[i][4]
        image = Image.open(BytesIO(image_data))
        size = change_picture_to_size(image)

        gold_frame_image = Image.open("homepage_design_pictures/gold_frame.png")
        gold_frame = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(light_image=gold_frame_image, size=size))
        gold_frame.grid(row=0, column=1, columnspan=2, padx=frame.winfo_width()/2-size[0], pady=20, sticky="SW")

        picture = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(light_image=image, size=size))
        picture.grid(row=0, column=1, columnspan=2, padx=frame.winfo_width()/2-size[0]-30, pady=40, sticky="SE")

        product_name = ctk.CTkLabel(frame, text=self.rows[i][1], font=("Broadway", 80))
        product_name = wrap_label_text_in_frame(frame, product_name, 0)
        product_name.grid(row=1, column=1, pady=10, sticky="E")

        price = ctk.CTkLabel(frame, text=str(self.rows[i][2])+"$", font=("Arial", 40))
        price.grid(row=1, column=2, stick="W")

        description = ctk.CTkLabel(frame, text=self.rows[i][3], font=("Arial", 40))
        description = wrap_label_text_in_frame(frame, description, 4)
        description.grid(row=2, column=1, columnspan=2, pady=10)

    def create_frames(self):
        for i in range(len(self.rows)):
            self.create_product_frame(i)
        self.conn.close()
