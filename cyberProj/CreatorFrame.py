import customtkinter as ctk
from PIL import Image
import InputDatabaseFrame2


class ColorMode:
    def __init__(self, background_frame):
        self.colors = ["default", "autumn", "cherry", "coffee", "green", "purple", "rime"]
        self.mode = "dark"
        self.mode_switch = ctk.CTkSwitch(master=background_frame, text="Dark Mode", onvalue="dark", offvalue="light",
                                         bg_color="transparent", command=lambda: self.choose_mode(
                                                                                 self.mode_switch.get()))

    def choose_mode(self, var):
        self.mode = var
        ctk.set_appearance_mode(self.mode)  # Modes: system (default), light, dark


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, root, background_frame):
        super().__init__(background_frame)
        self.root = root
        self.background_frame = background_frame
        self.check_boxs_var = [ctk.StringVar(value="off"), ctk.StringVar(value="off"), ctk.StringVar(value="off")]
        self.chosen_designs = ["none", "none", "none"]
        self.color = "default"
        self.pictures = [["p1", "p2", "p3"], ["p1", "p2", "p3"], ["p1", "p2", "p3"]]
        self.colors = ["default", "autumn", "cherry", "coffee", "green", "purple", "rime"]
        self.pic = [[f"color_designs_pic/metal-light.png", f"color_designs_pic/autumn-light.png",
                     f"color_designs_pic/cherry-light.png", f"color_designs_pic/coffee-light.png",
                     f"color_designs_pic/marsh-light.png", f"color_designs_pic/violet-light.png",
                     f"color_designs_pic/rime-light.png"],
                    [f"color_designs_pic/metal-dark.png", f"color_designs_pic/autumn-dark.png",
                     f"color_designs_pic/cherry-dark.png", f"color_designs_pic/coffee-dark.png",
                     f"color_designs_pic/marsh-dark.png", f"color_designs_pic/violet-dark.png",
                     f"color_designs_pic/rime-dark.png"]]
        self.database_frame = ctk.CTkFrame(background_frame)
        self.create_settings_frame()

    def print_pic(self):
        for i in range(len(self.pictures)):
            label_pic = ctk.CTkLabel(self, text=self.pictures[i][0])
            label_pic.grid(row=3, column=1+i, padx=20, pady=20)

    def choose_design(self, var, index):
        self.chosen_designs[index] = var
        label_pic = ctk.CTkLabel(self, text=self.pictures[index][int(var[-1])-1])
        label_pic.grid(row=3, column=1 + index, padx=20, pady=20)

    def choose_color(self, var):
        self.color = str(var)
        i = self.colors.index(self.color)
        self.print_color_pic(i)

    def print_color_pic(self, i):
        light_pic = ctk.CTkLabel(self, image=ctk.CTkImage(light_image=Image.open(self.pic[0][i]),
                                                          size=(200, 100)), text="")
        light_pic.grid(row=5, column=2)
        dark_pic = ctk.CTkLabel(self, image=ctk.CTkImage(light_image=Image.open(self.pic[1][i]),
                                                         size=(200, 100)), text="")
        dark_pic.grid(row=5, column=3)

    def get_database_tables(self):
        self.database_frame.destroy()
        self.database_frame = InputDatabaseFrame2.InputDatabaseFrame(self)
        self.database_frame.create_tables()

    def create_settings_frame(self):
        mode_switch = ColorMode(self.background_frame)
        mode_switch.mode_switch.place(x=10, y=10)

        self.background_frame.pack(fill="both", expand=True)
        self.background_frame.columnconfigure((0, 2), weight=1)

        self.grid(row=0, column=1, pady=10)
        self.columnconfigure((0, 4), weight=1)

        headline = ctk.CTkLabel(self, text="Welcome to AppSphere", font=("Harrington", 70))
        headline.grid(row=0, column=1, columnspan=3, padx=40, pady=20)

        explanation = ctk.CTkLabel(self, text="This is where you choose how your app will look. "
                                              "You can choose what your app will contain,"
                                              " the design of each part and the color theme. ")
        explanation.grid(row=1, column=1, columnspan=3, padx=20, pady=10)

        self.print_pic()

        check_boxs = [ctk.CTkCheckBox(self, text="Homepage", variable=self.check_boxs_var[0], onvalue="on",
                                      offvalue="off"),
                      ctk.CTkCheckBox(self, text="Catalog", variable=self.check_boxs_var[1], onvalue="on",
                                      offvalue="off"),
                      ctk.CTkCheckBox(self, text="Meeting System", variable=self.check_boxs_var[2], onvalue="on",
                                      offvalue="off")]

        for i in range(len(check_boxs)):
            check_boxs[i].grid(row=2, column=1+i, padx=20, pady=20)

        designs = ["design1", "design2", "design3"]

        designs_options = [ctk.CTkOptionMenu(self, values=designs, command=lambda x: self.choose_design(x, 0)),
                           ctk.CTkOptionMenu(self, values=designs, command=lambda x: self.choose_design(x, 1)),
                           ctk.CTkOptionMenu(self, values=designs, command=lambda x: self.choose_design(x, 2))]

        for i in range(len(designs_options)):
            designs_options[i].grid(row=4, column=1+i, padx=20, pady=20)

        color_options = ctk.CTkOptionMenu(self, values=self.colors, command=lambda x: self.choose_color(x))
        color_options.grid(row=5, column=1)
        self.print_color_pic(0)

        sub_button = ctk.CTkButton(self, text="Submit", command=self.get_database_tables)
        sub_button.grid(row=7, column=2, padx=20, pady=40)
