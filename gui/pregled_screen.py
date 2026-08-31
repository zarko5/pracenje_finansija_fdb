import os
import shutil
import uuid
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from .theme import *
from services import PoreskaService
from models import Transaction


class PregledScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        style = ttk.Style(self)
        style.configure("TLabelframe", font=FONT_MEDIUM)
        style.configure("TLabelframe.Label", font=FONT_MEDIUM)
        style.configure("TLabel", font=FONT_MEDIUM)
        style.configure("TButton", font=FONT_MEDIUM)
        style.configure("TEntry", font=FONT_MEDIUM)
        style.configure("TCombobox", font=FONT_MEDIUM)

        self._build_manual_form()
        self._build_poreska_form()
        self.load_categories()

    def _build_manual_form(self):
        frame = ttk.LabelFrame(self, text="Dodaj transakciju")
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Label(frame, text="Datum", font=FONT_MEDIUM).grid(row=0, column=0, sticky="w", padx=10, pady=6)
        self.date_entry = ttk.Entry(frame, font=FONT_MEDIUM)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(frame, text="Kategorija", font=FONT_MEDIUM).grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.manual_category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            frame,
            textvariable=self.manual_category_var,
            state="readonly",
            font=FONT_MEDIUM,
            width=28,
        )
        self.category_combo.grid(row=1, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(frame, text="Iznos", font=FONT_MEDIUM).grid(row=2, column=0, sticky="w", padx=10, pady=6)
        self.amount_entry = ttk.Entry(frame, font=FONT_MEDIUM)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(frame, text="Tip", font=FONT_MEDIUM).grid(row=3, column=0, sticky="w", padx=10, pady=6)
        self.type_var = tk.StringVar(value="rashod")
        ttk.Radiobutton(frame, text="Prihod", variable=self.type_var, value="prihod").grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(frame, text="Rashod", variable=self.type_var, value="rashod").grid(row=4, column=1, sticky="w")

        ttk.Label(frame, text="Opis", font=FONT_MEDIUM).grid(row=5, column=0, sticky="nw", padx=10, pady=6)
        self.desc_entry = tk.Text(frame, height=4, width=30, font=FONT_MEDIUM)
        self.desc_entry.grid(row=5, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(frame, text="Slika", font=FONT_MEDIUM).grid(row=6, column=0, sticky="w", padx=10, pady=6)
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(frame, textvariable=self.file_path, font=FONT_MEDIUM)
        self.file_entry.grid(row=6, column=1, padx=10, pady=6, sticky="ew")
        ttk.Button(frame, text="Izaberi fajl", command=self.choose_file).grid(row=6, column=2, padx=10, pady=6)

        ttk.Button(frame, text="Dodaj transakciju", command=self.add_manual_transaction).grid(row=7, column=1, sticky="e", padx=10, pady=10)

    def _build_poreska_form(self):
        frame = ttk.LabelFrame(self, text="Dodaj sa URL računa")
        frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ttk.Label(frame, text="URL", font=FONT_MEDIUM).grid(row=0, column=0, sticky="w", padx=10, pady=6)
        self.url_entry = ttk.Entry(frame, font=FONT_MEDIUM, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(frame, text="Kategorija", font=FONT_MEDIUM).grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.poreska_category_var = tk.StringVar()
        self.poreska_category_combo = ttk.Combobox(
            frame,
            textvariable=self.poreska_category_var,
            state="readonly",
            font=FONT_MEDIUM,
            width=28,
        )
        self.poreska_category_combo.grid(row=1, column=1, padx=10, pady=6, sticky="ew")

        ttk.Button(frame, text="Dodaj sa računa", command=self.add_invoice_from_url).grid(row=2, column=1, sticky="e", padx=10, pady=10)

    def load_categories(self):
        categories = self.controller.category_service.get_all_categories() or []
        names = [category.name for category in categories]

        if hasattr(self, "category_combo"):
            self.category_combo.configure(values=names)
        if hasattr(self, "poreska_category_combo"):
            self.poreska_category_combo.configure(values=names)

        if names:
            if hasattr(self, "manual_category_var"):
                self.manual_category_var.set(names[0])
            if hasattr(self, "poreska_category_var"):
                self.poreska_category_var.set(names[0])

    def choose_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.set(path)

    def copy_image_to_storage(self, source_path: str | None) -> str | None:
        if not source_path:
            return None

        if not os.path.exists(source_path):
            return None

        storage_dir = "db_images"
        os.makedirs(storage_dir, exist_ok=True)

        filename = f"{uuid.uuid4().hex}{os.path.splitext(source_path)[1]}"
        target_path = os.path.join(storage_dir, filename)
        shutil.copy2(source_path, target_path)
        return target_path

    def add_manual_transaction(self):
        amount_text = self.amount_entry.get().strip().replace(",", ".")
        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showwarning("Greška", "Unesite validan iznos")
            return

        if amount <= 0:
            messagebox.showwarning("Greška", "Iznos mora biti pozitivan broj")
            return

        category_name = self.manual_category_var.get()
        category = self.controller.category_service.get_category(category_name)
        if category is None:
            messagebox.showwarning("Greška", "Izaberite kategoriju")
            return

        description = self.desc_entry.get("1.0", "end").strip()
        transaction_date = self.date_entry.get().strip()

        if not transaction_date:
            messagebox.showwarning("Greška", "Unesite datum")
            return

        txn_type = self.type_var.get()
        signed_amount = abs(amount) if txn_type == "prihod" else -abs(amount)
        image_path = self.copy_image_to_storage(self.file_path.get() or None)

        transaction = Transaction(
            transaction_id=0,
            user_id=self.controller.current_id,
            category_id=category.id,
            amount=signed_amount,
            transaction_type="prihod" if txn_type == "prihod" else "trosak",
            transaction_date=transaction_date,
            desc=description,
            img_path=image_path,
        )

        success = self.controller.finance_service.add_transaction(transaction)
        if not success:
            messagebox.showwarning("Greška", "Dodavanje transakcije nije uspelo")
            return

        messagebox.showinfo("Uspešno", "Transakcija je dodata")
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete("1.0", tk.END)
        self.file_path.set("")

    def add_invoice_from_url(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Greška", "Unesite URL računa")
            return

        category_name = self.poreska_category_var.get()
        category = self.controller.category_service.get_category(category_name)
        if category is None:
            messagebox.showwarning("Greška", "Izaberite kategoriju za račun")
            return

        invoice_data = PoreskaService.parse_url_json(url)
        if invoice_data is None:
            messagebox.showwarning("Greška", "Nije moguće parsirati račun sa datog URL-a")
            return

        transactions = PoreskaService.parse_invoice_data(invoice_data, self.controller.current_id, category.id)
        if not transactions:
            messagebox.showwarning("Greška", "Na računu nema stavki za dodavanje")
            return

        saved = 0
        for transaction in transactions:
            if self.controller.finance_service.add_transaction(transaction):
                saved += 1

        messagebox.showinfo("Uspešno", f"Dodata je {saved} transakcija sa računa")
        self.url_entry.delete(0, tk.END)