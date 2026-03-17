import tkinter
import customtkinter as ctk
from icecream import ic
import requests
import urllib.request
from db import Database
from moviedb import MovieDB
from ui import constants
from ui.movie_frame import MovieFrame
from ui.checkbox_frame import GenreCheckBox

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.movie_list = Database.load_db()

        self.minsize(constants.APP_WIDTH,constants.APP_HEIGHT)

        # configure window
        self.title(constants.APP_TITLE)
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(0, weight=0, minsize=140)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        # sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure((0,1), weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text=constants.APP_TITLE,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nw")

        self.movie_cards()
        self.genre_checkbox()

    def genre_checkbox(self):
        movie_genres = MovieDB().get_genres()
        # checkbox buttons
        self.checkbox_frame = GenreCheckBox(
            self.sidebar_frame,
            values=list(movie_genres.values()),
            title=constants.GENRES,
            on_change=self.movie_card_frame.filter_by_genres
        )
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(70, 0), sticky="nsew")

    def movie_cards(self):
        # main frame
        self.movie_card_frame = MovieFrame(self, movies=self.movie_list.values())
        self.movie_card_frame.grid(row=0, column=1, sticky="nsew")

        #TODO: make cards clickable
