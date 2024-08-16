import tkinter
import customtkinter as ctk
from ui.checkbox_frame import GenreCheckBox
from ui.movie_card import MovieCard

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.minsize(800,500)

        # configure window
        self.title("My Movie Db")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="My Movie Db", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nw")

        # radio buttons
        self.checkbox_frame = GenreCheckBox(self, values=["horror", "comedy", "suspense"], title="Genres")
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # main frame
        self.movie_card_frame = MovieCard(self, title="The Dark Knight", year="2008", genre="Action", image_path="src/posters/fastx.jpeg")
        self.movie_card_frame.grid(row=0, column=1, padx=10, pady=10)
