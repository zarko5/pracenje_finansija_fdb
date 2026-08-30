import tkinter as tk
from tkinter import ttk,messagebox
from .theme import *


class KategorijeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ttk.Label(self, text="Kategorije", font=FONT_LARGE).grid(
            row=0, column=0, columnspan=2, pady=(20, 10)
        )

        self.input_category = ttk.Entry(self, font=FONT_MEDIUM)
        self.input_category.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

        ttk.Button(self, text="Dodaj kategoriju", command=self.add_category).grid(
            row=1, column=1, padx=(0, 20), pady=10, sticky="ew"
        )

        ttk.Button(self, text="Obrisi selektovano", command=self.delete_selected).grid(
            row=2, column=1, padx=(0, 20), pady=(0, 10), sticky="ew"
        )

        self.tree = ttk.Treeview(self, columns=("id", "naziv"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("naziv", text="Naziv")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("naziv", width=250)

        self.tree.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")

        self.load_categories()

    def add_category(self):
        name = self.input_category.get().strip()
        if not name:
            messagebox.showwarning("Greška", "Unesite naziv kategorije")
            return

        category = self.controller.category_service.add_category(name)
        if category is False or category is None:
            messagebox.showwarning("Greška", "Kategorija već postoji ili je došlo do greške")
            return

        self.input_category.delete(0, "end")
        self.load_categories()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Greška", "Selektujte kategoriju za brisanje")
            return

        item = self.tree.item(selected[0])
        category_name = item["values"][1]

        ok = self.controller.category_service.delete_category(category_name)
        if not ok:
            messagebox.showwarning("Greška", "Brisanje kategorije nije uspelo")
            return

        self.load_categories()

    def load_categories(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        categories = self.controller.category_service.get_all_categories()
        for category in categories:
            self.tree.insert("", "end", values=(category.id, category.name))