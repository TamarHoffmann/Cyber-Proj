import customtkinter as ctk
from PIL import Image, ImageOps
from io import BytesIO
import sqlite3
import textwrap
from tkinter.font import Font


def change_picture_to_size(picture, size):
    return picture.size[0] - (min(picture.size) - size), picture.size[1] - (min(picture.size) - size)


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


class HomePageDesign1:
    def __init__(self, background_frame):
        self.background_frame = background_frame
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM Homepage")
        self.rows = self.cursor.fetchall()
        self.create_frames()

    def create_left_picture_and_content(self, i):
        frame = ctk.CTkFrame(self.background_frame)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure((1, 3), weight=1)

        image_data = self.rows[i][4]
        image = Image.open(BytesIO(image_data))
        size = change_picture_to_size(image, 300)

        sparkles_image = Image.open("homepage_design_pictures/sparkles2.png")
        sparkles = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(
            light_image=sparkles_image, size=(size[0]+100, size[1]+190)))
        sparkles.grid(row=0, rowspan=3, column=0, sticky="NW")

        gold_frame_image = Image.open("homepage_design_pictures/gold_frame.png")
        gold_frame = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(light_image=gold_frame_image, size=size))
        gold_frame.grid(row=0, rowspan=3, column=0, padx=170, pady=80, sticky="NW")

        picture = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(light_image=image, size=size))
        picture.grid(row=0, rowspan=3, column=0, padx=200, pady=100, sticky="NE")

        headline = ctk.CTkLabel(frame, text=self.rows[i][2], font=("Broadway", 80))
        headline = wrap_label_text_in_frame(frame, headline, 0)
        headline.grid(row=0, column=2, sticky="S", pady=20)
        content = ctk.CTkLabel(frame, text=self.rows[i][3], font=("Arial", 40))
        content = wrap_label_text_in_frame(frame, content, 0)
        content.grid(row=1, column=2, sticky="N", pady=20)

    def create_right_picture_and_content(self, i):
        frame = ctk.CTkFrame(self.background_frame)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure((0, 2), weight=1)

        image_data = self.rows[i][4]
        image = Image.open(BytesIO(image_data))
        size = change_picture_to_size(image, 300)

        sparkles_image = ImageOps.mirror(Image.open("homepage_design_pictures/sparkles2.png"))
        sparkles = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(
            light_image=sparkles_image, size=(size[0] + 100, size[1] + 190)))
        sparkles.grid(row=0, rowspan=3, column=3, sticky="NE")

        gold_frame_image = Image.open("homepage_design_pictures/gold_frames.png")
        gold_frame = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(light_image=gold_frame_image,
                                                                     size=(size[0] + 40, size[1] + 40)))
        gold_frame.grid(row=0, rowspan=3, column=3, padx=150, pady=80, sticky="nsew")

        picture = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(light_image=image, size=size))
        picture.grid(row=0, rowspan=3, column=3, padx=170, pady=100, sticky="nsew")

        headline = ctk.CTkLabel(frame, text=self.rows[i][2], font=("Broadway", 80))
        headline = wrap_label_text_in_frame(frame, headline, 3)
        headline.grid(row=0, column=1, sticky="S", pady=20)
        content = ctk.CTkLabel(frame, text=self.rows[i][2], font=("Arial", 40))
        content = wrap_label_text_in_frame(frame, content, 3)
        content.grid(row=1, column=1, sticky="N", pady=20)

    def create_only_content(self, i):
        frame = ctk.CTkFrame(self.background_frame)
        frame.pack(side="top", fill="both", pady=10)
        frame.columnconfigure((0, 2), weight=1)

        bg_image = Image.open("homepage_design_pictures/gold_background.png")
        background_label = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(
            light_image=bg_image, size=(2000, 800)))
        background_label.grid(row=0, rowspan=3, column=0, columnspan=3, sticky="nsew")

        text_frame = ctk.CTkFrame(frame)
        text_frame.grid(row=1, column=1)

        headline = ctk.CTkLabel(text_frame, text=self.rows[i][2], font=("Broadway", 80))
        headline = wrap_label_text_in_frame(frame, headline, 4)
        headline.grid(row=0, column=1, pady=30, sticky="S")
        content = ctk.CTkLabel(text_frame, text=self.rows[i][3], font=("Arial", 40))
        content = wrap_label_text_in_frame(frame, content, 4)
        content.grid(row=1, column=1, pady=30, sticky="N")

    def create_pictures_only(self, i):
        frame = ctk.CTkFrame(self.background_frame)
        frame.pack(side="top", fill="both", pady=10)
        frame.columnconfigure((0, 4), weight=1)

        sparkles_image = Image.open("homepage_design_pictures/sparkles1.png")
        sparkles = ctk.CTkLabel(frame, text=self.rows[i][2], font=("Broadway", 80), image=ctk.CTkImage(
            light_image=sparkles_image, size=(1500, 400)))
        sparkles = wrap_label_text_in_frame(frame, sparkles, 4)
        sparkles.grid(row=0, column=0, columnspan=5, sticky="NW")

        for j in range(3):
            image_data = self.rows[i][4+j]
            image = Image.open(BytesIO(image_data))
            size = change_picture_to_size(image, 200)

            gold_frame_image = Image.open("homepage_design_pictures/gold_frame2.png")
            gold_frame = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(light_image=gold_frame_image,
                                                                         size=(size[0]+40, size[1]+80)))
            gold_frame.grid(row=1, column=j+1, padx=30)

            picture = ctk.CTkLabel(frame, text="", image=ctk.CTkImage(light_image=image, size=size))
            picture.grid(row=1, column=j+1, padx=30, pady=30)

    def create_frames(self):
        for i in range(len(self.rows)):
            method = getattr(self, f"create_{self.rows[i][1]}", None)
            if method is not None:
                method(i)
        self.conn.close()
