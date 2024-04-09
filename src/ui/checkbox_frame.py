import tkinter
import customtkinter as ctk

class GenreCheckBox(ctk.CTkFrame):
    def __init__(self, master, values, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.genres = values
        self.checkboxes = []
        self.title = title

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")

        for i, genre in enumerate(self.genres):
            checkbox = ctk.CTkCheckBox(self, text=genre)
            checkbox.grid(row=i+1, column=0, padx=20, pady=10, sticky="w")
            self.checkboxes.append(checkbox)

    def get(self) -> list[str]:
        checked_boxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_boxes.append(checkbox.cget("text"))
        return checked_boxes
