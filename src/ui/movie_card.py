from io import BytesIO
import logging
import tkinter as tk
import customtkinter as ctk
from PIL import Image, UnidentifiedImageError
import requests

from ui import constants

class MovieCard(ctk.CTkFrame):
    def __init__(self, master, title: str, year: str, genre: str, image_path: str):
        super().__init__(master, width=200, height=300, corner_radius=10)

        self.grid_propagate(False)
        self.pack_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self._visible = True
        self._hovered = False

        self.title = title
        self.year = year
        self.genre = genre

        # Movie poster
        self.image_path = self._load_poster_image(image_path)
        self.image = ctk.CTkImage(
            light_image=self.image_path,
            dark_image=self.image_path,
            size=(200,300)
        )

        self.image_label = ctk.CTkLabel(self, image=self.image, text="")
        self.image_label.grid(row=0, column=0, padx=10, sticky="ew")

        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text=self.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=180, justify="center"
        )
        self.title_label.place(relx=1.0, rely=1.0 ,x=0, y=-10)
        self.title_label.grid(row=1, column=0, padx=10, sticky="ew")

        # Year label
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

        # Genre label
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

        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)

        for child in self.winfo_children():
            child.bind("<Motion>", self._on_motion)
            child.bind("<Leave>", self._on_leave)


    def _is_child_of_card(self, widget):
        while widget is not None:
            if widget == self:
                return True
            widget = widget.master
        return False


    def _on_motion(self, event=None):
        if not self._hovered:
            self._hovered = True
            self.configure(
                fg_color=constants.HIGHLIGHT_COLOR,
                cursor="hand2"
            )


    def _on_leave(self, event=None):
        if self._hovered:
            self._hovered = False
            self.configure(
                fg_color=constants.REGULAR_COLOR,
                cursor=""
            )


    def _load_poster_image(self, poster_path: str):
        logging.info(f"loading poster for '{self.title}'")
        try:
            url = f"https://image.tmdb.org/t/p/original{poster_path}"
            response = requests.get(url)
            return Image.open(BytesIO(response.content))
        except UnidentifiedImageError:
            logging.warning(f"Could not identify the poster for '{self.title}', returning default poster")
            return Image.open(constants.DEFAULT_POSTER)


    def get(self) -> tuple[str, str, str, Image.Image]:
        return self.title, self.year, self.genre, self.image
