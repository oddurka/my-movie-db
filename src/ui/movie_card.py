import tkinter
import customtkinter as ctk

class MovieCard(ctk.CTkFrame):
    def __init__(self, master, title, year, genre):
        super().__init__(master, width=200, height=300, corner_radius=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.title = title
        self.year = year
        self.genre = genre

        self.title_label = ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.year_label = ctk.CTkLabel(self, text=self.year, fg_color="gray30")
        self.year_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.genre_label = ctk.CTkLabel(self, text=self.genre, fg_color="gray30")
        self.genre_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

    def get(self) -> tuple[str, str, str]:
        return self.title, self.year, self.genre
