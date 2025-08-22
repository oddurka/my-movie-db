import tkinter
import customtkinter as ctk
from PIL import Image

class MovieCard(ctk.CTkFrame):
    def __init__(self, master, title: str, year: str, genre: str, image_path: str):
        super().__init__(master, width=200, height=300, corner_radius=10)

        self.grid_propagate(False)
        self.pack_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.title = title
        self.year = year
        self.genre = genre
        #self.image = ctk.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(200,300))
        self.image = ctk.CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(200,300)
        )

        self.image_label = ctk.CTkLabel(self, image=self.image, text="")
        self.image_label.grid(row=0, column=0, padx=10, sticky="ew")

        self.title_label = ctk.CTkLabel(
            self,
            text=self.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=180, justify="center"
        )
        self.title_label.place(relx=1.0, rely=1.0 ,x=0, y=-10)
        self.title_label.grid(row=1, column=0, padx=10, sticky="ew")

        self.year_label = ctk.CTkLabel(
            self,
            text=self.year,
            fg_color="gray30"
        )
        self.year_label.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.genre_label = ctk.CTkLabel(
            self,
            text=self.genre,
            fg_color="gray30"
        )
        self.genre_label.grid(
            row=3,
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew"
        )

    def get(self) -> tuple[str, str, str, Image.Image]:
        return self.title, self.year, self.genre, self.image
