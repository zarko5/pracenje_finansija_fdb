import os
import shutil
import uuid
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from .theme import *
from models import Transaction


class TransakcijeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        style = ttk.Style(self)
        style.configure("TLabel", font=FONT_MEDIUM)
        style.configure("TButton", font=FONT_MEDIUM)
        style.configure("TEntry", font=FONT_MEDIUM)
        style.configure("TCombobox", font=FONT_MEDIUM)
        style.configure("Treeview", font=FONT_MEDIUM, rowheight=28)
        style.configure("Treeview.Heading", font=FONT_MEDIUM)

        ttk.Label(self, text="Transakcije", font=FONT_LARGE).grid(
            row=0, column=0, columnspan=2, pady=(20, 10)
        )

        self.tree = ttk.Treeview(
            self,
            columns=("id", "datum", "kategorija", "iznos", "tip", "opis", "slika"),
            show="headings",
            height=16,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("datum", text="Datum")
        self.tree.heading("kategorija", text="Kategorija")
        self.tree.heading("iznos", text="Iznos")
        self.tree.heading("tip", text="Tip")
        self.tree.heading("opis", text="Opis")
        self.tree.heading("slika", text="Slika")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("datum", width=110, anchor="center")
        self.tree.column("kategorija", width=150)
        self.tree.column("iznos", width=110, anchor="center")
        self.tree.column("tip", width=100, anchor="center")
        self.tree.column("opis", width=320)
        self.tree.column("slika", width=110, anchor="center")

        self.tree.grid(row=1, column=0, padx=(20, 0), pady=(10, 20), sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns", pady=(10, 20))
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20), padx=20, sticky="ew")

        ttk.Button(btn_frame, text="Uredi selektovano", command=self.edit_selected).pack(side="left", padx=(0, 10))
        ttk.Button(btn_frame, text="Obriši selektovano", command=self.delete_selected).pack(side="left")
        ttk.Button(btn_frame, text="Prikaži sliku", command=self.show_selected_image).pack(side="left", padx=(10, 0))

        self.load_transactions()

    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        transactions = self.controller.finance_service.get_user_transactions(self.controller.current_id)
        if not transactions:
            return

        for transaction in transactions:
            category = self.controller.category_service.get_category_by_id(transaction.category_id)
            category_name = category.name if category else "-"
            image_label = "Da" if transaction.receipt_image_path else "Ne"
            self.tree.insert(
                "",
                "end",
                values=(
                    transaction.id,
                    transaction.date,
                    category_name,
                    f"{transaction.amount:.2f}",
                    "Prihod" if transaction.type == "prihod" else "Trosak",
                    transaction.description or "-",
                    image_label,
                ),
            )

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Greška", "Selektujte transakciju za brisanje")
            return

        item = self.tree.item(selected[0])
        transaction_id = item["values"][0]
        transaction = self.controller.finance_service.get_transaction(int(transaction_id))

        if transaction is None:
            messagebox.showwarning("Greška", "Transakcija nije pronađena")
            return

        confirmed = messagebox.askyesno("Potvrda", "Da li ste sigurni da želite da izbrišete ovu transakciju?")
        if not confirmed:
            return

        ok = self.controller.finance_service.delete_transaction(transaction)
        if not ok:
            messagebox.showwarning("Greška", "Brisanje transakcije nije uspelo")
            return

        self.load_transactions()

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

    def show_selected_image(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Greška", "Selektujte transakciju")
            return

        transaction_id = int(self.tree.item(selected[0])["values"][0])
        transaction = self.controller.finance_service.get_transaction(transaction_id)
        if transaction is None or not transaction.receipt_image_path:
            messagebox.showinfo("Info", "Za ovu transakciju ne postoji slika")
            return

        if not os.path.exists(transaction.receipt_image_path):
            messagebox.showwarning("Greška", "Slika više ne postoji na disku")
            return

        image = Image.open(transaction.receipt_image_path)
        image.thumbnail((500, 500))

        preview = tk.Toplevel(self)
        preview.title("Pregled slike")
        preview.geometry("600x600")
        apply_popup_theme(preview)

        photo = ImageTk.PhotoImage(image)
        image_frame = tk.Frame(preview, bg=APP_BG)
        image_frame.pack(fill="both", expand=True, padx=12, pady=12)

        label = tk.Label(image_frame, image=photo, bg=APP_BG, compound="center")
        label.image = photo
        label.pack(fill="both", expand=True)

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Greška", "Selektujte transakciju za uređivanje")
            return

        item = self.tree.item(selected[0])
        transaction_id = int(item["values"][0])
        transaction = self.controller.finance_service.get_transaction(transaction_id)

        if transaction is None:
            messagebox.showwarning("Greška", "Transakcija nije pronađena")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Uredi transakciju")
        dialog.geometry("460x420")
        apply_popup_theme(dialog)

        current_image_path = tk.StringVar(value=transaction.receipt_image_path or "")

        ttk.Label(dialog, text="Datum", font=FONT_MEDIUM).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        date_var = tk.StringVar(value=transaction.date)
        ttk.Entry(dialog, textvariable=date_var, font=FONT_MEDIUM).grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(dialog, text="Kategorija", font=FONT_MEDIUM).grid(row=1, column=0, padx=10, pady=8, sticky="w")
        categories = self.controller.category_service.get_all_categories() or []
        names = [category.name for category in categories]
        category_name = self.controller.category_service.get_category_by_id(transaction.category_id)
        category_var = tk.StringVar(value=category_name.name if category_name else "")
        combo = ttk.Combobox(dialog, textvariable=category_var, values=names, state="readonly", font=FONT_MEDIUM)
        combo.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(dialog, text="Iznos", font=FONT_MEDIUM).grid(row=2, column=0, padx=10, pady=8, sticky="w")
        amount_var = tk.StringVar(value=str(abs(transaction.amount)))
        ttk.Entry(dialog, textvariable=amount_var, font=FONT_MEDIUM).grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(dialog, text="Tip", font=FONT_MEDIUM).grid(row=3, column=0, padx=10, pady=8, sticky="w")
        type_var = tk.StringVar(value="prihod" if transaction.type == "prihod" else "trosak")
        ttk.Radiobutton(dialog, text="Prihod", variable=type_var, value="prihod").grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(dialog, text="Trosak", variable=type_var, value="trosak").grid(row=4, column=1, sticky="w")

        ttk.Label(dialog, text="Opis", font=FONT_MEDIUM).grid(row=5, column=0, padx=10, pady=8, sticky="nw")
        desc_var = tk.StringVar(value=transaction.description or "")
        ttk.Entry(dialog, textvariable=desc_var, font=FONT_MEDIUM).grid(row=5, column=1, padx=10, pady=8, sticky="ew")

        ttk.Label(dialog, text="Slika", font=FONT_MEDIUM).grid(row=6, column=0, padx=10, pady=8, sticky="w")
        image_entry = ttk.Entry(dialog, textvariable=current_image_path, font=FONT_MEDIUM)
        image_entry.grid(row=6, column=1, padx=10, pady=8, sticky="ew")
        ttk.Button(dialog, text="Izaberi sliku", command=lambda: current_image_path.set(filedialog.askopenfilename() or current_image_path.get())).grid(row=6, column=2, padx=10, pady=8)

        def save_change():
            try:
                amount = float(amount_var.get().replace(",", "."))
            except ValueError:
                messagebox.showwarning("Greška", "Unesite validan iznos")
                return

            category_name = category_var.get()
            category = self.controller.category_service.get_category(category_name)
            if category is None:
                messagebox.showwarning("Greška", "Odaberite validnu kategoriju")
                return

            new_image_path = self.copy_image_to_storage(current_image_path.get()) if current_image_path.get() else None
            if current_image_path.get() and new_image_path is None:
                messagebox.showwarning("Greška", "Nije moguće kopirati izabranu sliku")
                return

            if transaction.receipt_image_path and current_image_path.get() and os.path.exists(transaction.receipt_image_path):
                os.remove(transaction.receipt_image_path)

            updated = Transaction(
                transaction_id=transaction.id,
                user_id=transaction.user_id,
                category_id=category.id,
                amount=abs(amount) if type_var.get() == "prihod" else -abs(amount),
                transaction_type="prihod" if type_var.get() == "prihod" else "trosak",
                transaction_date=date_var.get(),
                desc=desc_var.get(),
                img_path=new_image_path or transaction.receipt_image_path,
            )

            ok = self.controller.finance_service.update_transaction(updated)
            if not ok:
                messagebox.showwarning("Greška", "Nije uspela izmena transakcije")
                return

            self.load_transactions()
            dialog.destroy()

        ttk.Button(dialog, text="Sačuvaj", command=save_change).grid(row=7, column=1, sticky="e", padx=10, pady=(12, 10))
        dialog.columnconfigure(1, weight=1)
