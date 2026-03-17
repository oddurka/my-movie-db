from io import BytesIO
import logging
import tkinter
import urllib.request
from PIL import Image
import customtkinter as ctk
import requests

from ui.movie_card import MovieCard

CARD_WIDTH = 220   # minimum width of a MovieCard
CARD_PADX = 10
CARD_PADY = 10


class MovieFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, movies):
        super().__init__(master)

        self.movies = movies
        self.movie_cards = []
        self.current_columns = 0

        for movie in self.movies:
            print(f"Loading movie '{movie['title']}'")
            card = MovieCard(
                self,
                movie["title"],
                movie["year"],
                movie["genre"],
                movie["poster_path"]
            )
            card.genre = movie["genre"]
            self.movie_cards.append(card)

        self.bind("<Configure>", self._on_resize)
        self._regrid()

    def _on_resize(self, event=None):
        self._regrid()

    def _regrid(self):
        if not self.movie_cards:
            return

        width = self.winfo_width()
        if width <= 1:
            return

        card_width = self.movie_cards[0].winfo_reqwidth()
        columns = max(1, width // (card_width + CARD_PADX * 2))

        self.current_columns = columns

        for card in self.movie_cards:
            card.grid_forget()

        visible_cards = [c for c in self.movie_cards if c._visible]

        for i, card in enumerate(visible_cards):
            row = i // columns
            col = i % columns
            card.grid(
                row=row,
                column=col,
                padx=CARD_PADX,
                pady=CARD_PADY,
                sticky="n"
            )

        self.update_idletasks()
        self._parent_canvas.configure(
            scrollregion=self._parent_canvas.bbox("all")
        )

    def filter_by_genres(self, selected_genres: list[str]):
        selected = set(selected_genres)

        for card in self.movie_cards:
            if not selected_genres:
                card._visible = True
            else:
                genres = (
                    card.genre if isinstance(card.genre, (list, tuple))
                    else [g.strip() for g in card.genre.split(",")]
                )
                card._visible = bool(selected.intersection(genres))

        self._regrid()

    def get(self) -> list[str]:
        selected = []
        for card in self.movie_cards:
            if card.get() == 1:
                selected.append(card.cget("text"))
        return selected
