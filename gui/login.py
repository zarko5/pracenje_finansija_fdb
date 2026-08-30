import tkinter as tk
from tkinter import ttk,messagebox
from .theme import *


class LoginEkran(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_id = None


        label1 = ttk.Label(self, text="Login",font=FONT_LARGE)
        label1.grid(row=0,column=0, columnspan=2, pady=10)

        # red = ttk.Frame(self)
        # red.pack(fill="x", padx=20, pady=5)


        label2 = ttk.Label(self, text="Korisnicko ime", font=FONT_MEDIUM)
        label2.grid(row=1,column=0,padx=10,pady=5)

        self.input_username = ttk.Entry(self, font=FONT_MEDIUM)
        self.input_username.grid(row=1, column=1,padx=10,pady=5)

        label3 = ttk.Label(self, text="Lozinka", font=FONT_MEDIUM)
        label3.grid(row=2,column=0,padx=10,pady=5)

        self.input_pass = ttk.Entry(self, font=FONT_MEDIUM,show="*")
        self.input_pass.grid(row=2,column=1,padx=10,pady=5)

        login_btn = ttk.Button(self, text="Uloguj se", command=self.btn_click)
        login_btn.grid(row=3,column=1,padx=10,pady=5)



        ### registracija    
        label_reg = ttk.Label(self, text="Registracija",font=FONT_LARGE)
        label_reg.grid(row=5,column = 0, columnspan=2 ,padx=10,pady=(50,20))

        label4 = ttk.Label(self, text="Korisnicko ime", font=FONT_MEDIUM)
        label4.grid(row=6,column = 0,padx=10,pady=5)

        self.input_reg_username = ttk.Entry(self, font=FONT_MEDIUM)
        self.input_reg_username.grid(row=6,column = 1,padx=10,pady=5)

        label5 = ttk.Label(self, text="Lozinka", font=FONT_MEDIUM)
        label5.grid(row=7,column = 0,padx=10,pady=5)


        self.input_reg_pass1 = ttk.Entry(self, font=FONT_MEDIUM,show="*")
        self.input_reg_pass1.grid(row=7,column = 1,padx=10,pady=5)


        label5 = ttk.Label(self, text="Ponovi lozinku", font=FONT_MEDIUM)
        label5.grid(row=8,column = 0,padx=10,pady=5)

        self.input_reg_pass2 = ttk.Entry(self, font=FONT_MEDIUM,show="*")
        self.input_reg_pass2.grid(row=8,column = 1,padx=10,pady=5)

        register_btn = ttk.Button(self, text="Registruj se", command=self.btn_reg_click)
        register_btn.grid(row=9,column=1, padx=10,pady=5)

        # login_btn = ttk.Button(self, text="Uloguj se", command=self.btn_click)


    def btn_click(self):
        ret = self.controller.auth_gui(self.input_username.get(), self.input_pass.get())
        if ret == False:
            messagebox.showwarning(message="Netacni kredencijali")
        else:
            # ako je okej, vratio se userid, treba da prelazimo na sledeci ekran i da passujemo usera
            self.controller.open_main(ret) 
        # pass

    def btn_reg_click(self):
        # check usera
        usr = self.input_reg_username.get()
        p1 = self.input_reg_pass1.get()
        p2 = self.input_reg_pass2.get()

        if usr == "":
            messagebox.showwarning(message="Korisnicko ime je prazno")
            return
        if p1 != p2:
            messagebox.showwarning(message="Lozinke se ne poklapaju")
            return

        ret = self.controller.register_gui(usr,p1)
        if ret is False:
            messagebox.showwarning(message="Greska pri registraciji")
            return

        self.input_reg_pass2.delete(0, tk.END)
        self.input_reg_pass1.delete(0,tk.END)

        self.input_username.delete(0,tk.END)
        self.input_username.insert(0,usr)
        self.input_reg_username.delete(0,tk.END)

