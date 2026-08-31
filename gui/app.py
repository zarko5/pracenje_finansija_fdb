import tkinter as tk
from tkinter import ttk
from gui.login import LoginEkran
from gui.kategorije_screen import KategorijeScreen
from gui.pregled_screen import PregledScreen
from gui.izvestaji_screen import IzvestajiScreen
from gui.transakcije_screen import TransakcijeScreen
from .theme import *
import services

class App(tk.Tk):
    def __init__(self,db):
        super().__init__()

        apply_global_theme(self)

        self.title("Aplikacija za pracenje finansija")
        self.geometry("1920x1000")
        self.current_id = None
        

        self.auth_service = services.AuthService(db)
        self.finance_service = services.FinanceService(db)
        self.category_service = services.CategoryService(db)
        # poreska je staticna ugl tkd

        self.notebook = None

        self.LoginScreen = LoginEkran(parent=self,controller=self)
        self.LoginScreen.pack(fill="both", expand=True)


    def auth_gui(self, username: str, password: str) -> bool | int:
        usr = self.auth_service.authenticate_user(username, password)
        if usr is False:
            return False
        else: 
            return usr.id

    def register_gui(self, username: str, password: str) -> bool:
        if self.auth_service.get_user(username) is not None:
            ## korisnik vec postoji situacija
            return False

        if self.auth_service.register_user(username, password) is not None:
            return True

    def open_main(self,user_id: int):
        self.current_id = user_id
        if self.notebook is None:
            self.LoginScreen.pack_forget()
            
            self.notebook = ttk.Notebook(self)
            self.notebook.pack(fill="both", expand=True)

            self._build_tabs()

        self.notebook.tkraise()

    def _build_tabs(self):
        self.pregled_tab = PregledScreen(self.notebook,self)
        self.notebook.add(self.pregled_tab, text="Pregled")

        self.kategorije_tab = KategorijeScreen(self.notebook,self)
        self.notebook.add(self.kategorije_tab, text="Kategorije")

        self.izvestaji_tab = IzvestajiScreen(self.notebook, self)
        self.notebook.add(self.izvestaji_tab, text="Izvestaji")

        self.transakcije_tab = TransakcijeScreen(self.notebook, self)
        self.notebook.add(self.transakcije_tab, text="Transakcije")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event=None):
        selected_tab = self.notebook.nametowidget(self.notebook.select())

        if hasattr(selected_tab, "load_transactions"):
            selected_tab.load_transactions()

        if hasattr(selected_tab, "load_report_data"):
            selected_tab.load_report_data()

        if hasattr(selected_tab, "load_categories"):
            selected_tab.load_categories()
