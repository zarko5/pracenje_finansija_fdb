import tkinter as tk
from tkinter import ttk
from .theme import *


class LoginEkran(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # self.auth_service = auth_service
        # self.finance_service = finance_service
        # self.master = master
        # self.master.title("Login")
        label1 = ttk.Label(self, text="Login",font=FONT_LARGE)
        label1.pack(pady=10)

        label2 = ttk.Label(self, text="lab2", font=FONT_MEDIUM)
        label2.pack(pady=10)
