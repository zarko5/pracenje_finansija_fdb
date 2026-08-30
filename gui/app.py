import tkinter as tk
from tkinter import ttk
from gui.login import LoginEkran
from .theme import *
import services

class App(tk.Tk):
    def __init__(self,db):
        super().__init__()

        self.title("Aplikacija za pracenje finansija")
        self.geometry("1270x720")

        self.auth_service = services.AuthService(db)
        self.finance_service = services.FinanceService(db)
        self.category_service = services.CategoryService(db)
        # poreska je staticna ugl tkd

        # self.notebook = ttk.Notebook(self)
        # self.notebook.pack(fill="both", expand=True)

        self.LoginScreen = LoginEkran(parent=self,controller=self)
        self.LoginScreen.pack(fill="both", expand=True)

        # self.dashboard_tab = DashboardScreen(self.notebook, controller=self)
        # self.add_receipt_tab = AddReceiptScreen(self.notebook, controller=self)

        # self.notebook.add(self.dashboard_tab, text=" Pregled (Dashboard)")
        # self.notebook.add(self.add_receipt_tab, text="Dodaj račun")