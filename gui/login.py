import tkinter as tk
from tkinter import ttk
from .theme import *


class LoginEkran(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        label1 = ttk.Label(self, text="Login",font=FONT_LARGE)
        label1.pack(pady=10)

        red = ttk.Frame(self)
        red.pack(fill="x", padx=20, pady=5)


        label2 = ttk.Label(red, text="Korisnicko ime",width=20,anchor="w", font=FONT_MEDIUM)
        label2.pack(side="left")

        input_username = ttk.Entry(red, font=FONT_MEDIUM)
        input_username.pack(side="left")

        label3 = ttk.Label(red, text="Lozinka", anchor="w", width=20, font=FONT_MEDIUM)
        label3.pack(side="left")

        input_pass = ttk.Entry(red, font=FONT_MEDIUM,show="*")
        input_pass.pack(pady=10)

        login_btn = ttk.Button(self, text="Uloguj se", command=self.btn_click)
        login_btn.pack(pady=10)



        ### registracija
        label_reg = ttk.Label(self, text="Registracija",font=FONT_LARGE)
        label_reg.pack(pady=10)

        label4 = ttk.Label(self, text="Korisnicko ime", font=FONT_MEDIUM)
        label4.pack(pady=10,padx=10)

        input_username2 = ttk.Entry(self, font=FONT_MEDIUM)
        input_username2.pack(pady=10)

        label5 = ttk.Label(self, text="Lozinka", font=FONT_MEDIUM)
        label5.pack(pady=(10,15))


        input_pass2 = ttk.Entry(self, font=FONT_MEDIUM,show="*")
        input_pass2.pack(pady=10)


        login_btn = ttk.Button(self, text="Uloguj se", command=self.btn_click)


    def btn_click(self):
        
        pass

