import tkinter
import customtkinter as ctk

class GenreCheckBox(ctk.CTkScrollableFrame):
    def __init__(self, master, values, title, on_change):
        super().__init__(master)

        self.on_change = on_change
        self.checkboxes = []

        self.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self,
            text=title,
            fg_color="gray30",
            corner_radius=6
        )
        title_label.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")

        for i, genre in enumerate(values):
            checkbox = ctk.CTkCheckBox(
                self,
                text=genre,
                command=self._on_change
            )
            checkbox.grid(row=i+1, column=0, padx=20, pady=10, sticky="w")
            self.checkboxes.append(checkbox)

    def _on_change(self):
        self.on_change(self.get())

    def get(self) -> list[str]:
        return [
            checkbox.cget("text")
            for checkbox in self.checkboxes
            if checkbox.get() == 1
        ]
