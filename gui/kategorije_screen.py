import tkinter as tk
from tkinter import ttk,messagebox
from .theme import *


class KategorijeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


        style = ttk.Style(self)
        style.configure("TLabel", font=FONT_MEDIUM)
        style.configure("TButton", font=FONT_MEDIUM)
        style.configure("TEntry", font=FONT_MEDIUM)
        style.configure("Treeview", font=FONT_MEDIUM,rowheight=30)
        style.configure("Treeview.Heading", font=FONT_MEDIUM)

        ttk.Label(self, text="Kategorije", font=FONT_LARGE).grid(
            row=0, column=0, columnspan=2, pady=(20, 10)
        )

        self.input_category = ttk.Entry(self, font=FONT_MEDIUM)
        self.input_category.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

        ttk.Button(self, text="Dodaj kategoriju", command=self.add_category).grid(
            row=1, column=1, padx=(0, 20), pady=10, sticky="ew"
        )

        ttk.Button(self, text="Izmeni selektovano", command=self.edit_selected).grid(
            row=2, column=1, padx=(0, 20), pady=(0, 10), sticky="ew"
        )


        ttk.Button(self, text="Obrisi selektovano", command=self.delete_selected).grid(
            row=3, column=1, padx=(0, 20), pady=(0, 10), sticky="ew"
        )



        self.tree = ttk.Treeview(self, columns=("id", "naziv"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("naziv", text="Naziv")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("naziv", width=250)

        self.tree.grid(row=4, column=0, columnspan=2, padx=(20,0), pady=(10, 30), sticky="nsew")

        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(row=4, column=2, sticky="ns", pady=(10, 30))

        self.tree.configure(yscrollcommand=self.tree_scroll.set)


        self.load_categories()

    def add_category(self):
        name = self.input_category.get().strip()
        if not name:
            messagebox.showwarning("Greska", "Unesite naziv kategorije")
            return

        category = self.controller.category_service.add_category(name)
        if category is False or category is None:
            messagebox.showwarning("Greska", "Kategorija već postoji ili je došlo do greske")
            return

        self.input_category.delete(0, "end")
        self.load_categories()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Greska", "Selektujte kategoriju za brisanje")
            return

        item = self.tree.item(selected[0])
        category_name = item["values"][1]

        ok = self.controller.category_service.delete_category(category_name)
        if not ok:
            messagebox.showwarning("Greska", "Brisanje kategorije nije uspelo")
            return

        self.load_categories()

    def edit_selected(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Greska", "Selektujte kategoriju za izmenu")
            return
        item = self.tree.item(selected[0])
        category_name = item["values"][1]

        new_name = self.input_category.get().strip()
        if not new_name:
            messagebox.showwarning("Greska", "Unesite naziv kategorije")
            return

        cat = self.controller.category_service.get_category(category_name)
        ok = self.controller.category_service.update_category(cat.id, new_name)

        if not ok:
            messagebox.showwarning("Greska", "Izmena kategorije nije uspela")
            return
        self.load_categories()

        
    def load_categories(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        categories = self.controller.category_service.get_all_categories()
        for category in categories:
            self.tree.insert("", "end", values=(category.id, category.name))