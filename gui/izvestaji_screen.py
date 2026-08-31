import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .theme import *


class IzvestajiScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, minsize=52)
        self.columnconfigure(1, weight=0)

        style = ttk.Style(self)
        style.configure("TLabelframe", background=APP_BG, font=FONT_MEDIUM)
        style.configure("TLabelframe.Label", background=APP_BG, foreground=APP_TEXT, font=FONT_MEDIUM)
        style.configure("TLabel", background=APP_BG, foreground=APP_TEXT, font=FONT_MEDIUM)
        style.configure("TButton", background=APP_PANEL, foreground=APP_TEXT, font=FONT_MEDIUM)
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", font=FONT_MEDIUM, rowheight=26)
        style.configure("Treeview.Heading", font=FONT_MEDIUM)

        self.header = ttk.Label(self, text="Izveštaji", font=FONT_LARGE, padding=(0, 4, 0, 2))
        self.header.grid(row=0, column=0, padx=20, pady=(16, 10), sticky="w")

        self.export_frame = tk.Frame(self, bg=APP_BG)
        self.export_frame.grid(row=0, column=1, padx=(0, 20), pady=(16, 10), sticky="e")

        self.export_excel_button = ttk.Button(self.export_frame, text="Export Excel", command=self.export_excel_report)
        self.export_excel_button.pack(side="left", padx=(0, 8))

        self.export_button = ttk.Button(self.export_frame, text="Export CSV", command=self.export_csv_report)
        self.export_button.pack(side="left")

        self.summary_frame = tk.Frame(self, bg=APP_BG)
        self.summary_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
        self.summary_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.cards = {}
        self.cards["income"] = self._create_summary_card("Ukupni prihodi", "0.00", "#d9f7e8")
        self.cards["expense"] = self._create_summary_card("Ukupni rashodi", "0.00", "#f9dcd9")
        self.cards["balance"] = self._create_summary_card("Saldo", "0.00", "#e8ebff")
        self.cards["count"] = self._create_summary_card("Broj transakcija", "0", "#f2ebd7")

        self.cards["income"].grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.cards["expense"].grid(row=0, column=1, padx=10, sticky="ew")
        self.cards["balance"].grid(row=0, column=2, padx=10, sticky="ew")
        self.cards["count"].grid(row=0, column=3, padx=(10, 0), sticky="ew")

        self.monthly_frame = ttk.LabelFrame(self, text="Mesečni grafik")
        self.monthly_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.monthly_canvas = tk.Canvas(self.monthly_frame, width=560, height=260, bg=APP_BG, highlightthickness=0)
        self.monthly_canvas.pack(fill="both", expand=True, padx=14, pady=(14, 10))

        self.monthly_tree = ttk.Treeview(self.monthly_frame, columns=("mesec", "prihod", "rashod", "saldo"), show="headings", height=5)
        self.monthly_tree.heading("mesec", text="Mesec")
        self.monthly_tree.heading("prihod", text="Prihod")
        self.monthly_tree.heading("rashod", text="Rashod")
        self.monthly_tree.heading("saldo", text="Saldo")
        self.monthly_tree.column("mesec", width=120, anchor="center")
        self.monthly_tree.column("prihod", width=100, anchor="center")
        self.monthly_tree.column("rashod", width=100, anchor="center")
        self.monthly_tree.column("saldo", width=100, anchor="center")
        self.monthly_tree.pack(fill="x", padx=10, pady=(0, 8))

        self.pie_frame = ttk.LabelFrame(self, text="Prihodi vs rashodi")
        self.pie_frame.grid(row=2, column=1, padx=(0, 20), pady=(0, 10), sticky="nsew")
        self.pie_canvas = tk.Canvas(self.pie_frame, width=460, height=260, bg=APP_BG, highlightthickness=0)
        self.pie_canvas.pack(fill="both", expand=True, padx=14, pady=(14, 10))

        self.category_frame = ttk.LabelFrame(self, text="Rashodi po kategorijama")
        self.category_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.category_tree = ttk.Treeview(self.category_frame, columns=("kategorija", "iznos"), show="headings", height=7)
        self.category_tree.heading("kategorija", text="Kategorija")
        self.category_tree.heading("iznos", text="Iznos")
        self.category_tree.column("kategorija", width=220, anchor="w")
        self.category_tree.column("iznos", width=140, anchor="center")
        self.category_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.recent_frame = ttk.LabelFrame(self, text="Poslednje transakcije")
        self.recent_frame.grid(row=3, column=1, padx=(0, 20), pady=(0, 20), sticky="nsew")
        self.recent_tree = ttk.Treeview(self.recent_frame, columns=("datum", "kategorija", "opis", "iznos"), show="headings", height=7)
        self.recent_tree.heading("datum", text="Datum")
        self.recent_tree.heading("kategorija", text="Kategorija")
        self.recent_tree.heading("opis", text="Opis")
        self.recent_tree.heading("iznos", text="Iznos")
        self.recent_tree.column("datum", width=120, anchor="center")
        self.recent_tree.column("kategorija", width=180, anchor="w")
        self.recent_tree.column("opis", width=260, anchor="w")
        self.recent_tree.column("iznos", width=120, anchor="center")
        self.recent_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_report_data()

    def _create_summary_card(self, title, value, color):
        frame = tk.Frame(self.summary_frame, bg=color, bd=1, relief="solid", padx=12, pady=12)
        frame.columnconfigure(0, weight=1)

        title_label = tk.Label(frame, text=title, bg=color, fg=APP_TEXT, font=FONT_SMALL)
        title_label.grid(row=0, column=0, sticky="w")

        value_label = tk.Label(frame, text=value, bg=color, fg=APP_TEXT, font=(FONT_FAMILY, 24, "bold"))
        value_label.grid(row=1, column=0, sticky="w", pady=(8, 0))

        frame.title_label = title_label
        frame.value_label = value_label
        return frame

    def _money(self, value):
        return f"{float(value):.2f}"

    def _category_name_for_id(self, category_id):
        category = self.controller.category_service.get_category_by_id(category_id)
        if category is None:
            return "-"
        return category.name

    def _draw_monthly_chart(self, monthly_data):
        self.monthly_canvas.delete("all")

        if not monthly_data:
            self.monthly_canvas.create_text(280, 120, text="Nema podataka", fill=APP_TEXT, font=(FONT_FAMILY, 12))
            return

        labels = list(monthly_data.keys())
        incomes = [monthly_data[m]["income"] for m in labels]
        expenses = [monthly_data[m]["expense"] for m in labels]
        max_value = max(max(incomes or [0]), max(expenses or [0]), 1)

        chart_x0, chart_y0 = 120, 56
        chart_width = 390
        chart_height = 150
        bar_width = 18
        x_step = (chart_width - 24) / max(len(labels), 1)

        self.monthly_canvas.create_line(chart_x0, chart_y0 + chart_height, chart_x0 + chart_width, chart_y0 + chart_height, fill="#4a4a4a", width=2)
        self.monthly_canvas.create_line(chart_x0, chart_y0, chart_x0, chart_y0 + chart_height, fill="#4a4a4a", width=2)

        for tick in range(0, 6):
            value = (max_value / 5) * tick
            y = chart_y0 + chart_height - (value / max_value) * chart_height
            self.monthly_canvas.create_line(chart_x0 - 4, y, chart_x0, y, fill="#666666")
            self.monthly_canvas.create_text(chart_x0 - 14, y, text=f"{value:.0f}", anchor="e", fill=APP_TEXT, font=(FONT_FAMILY, 11, "bold"))

        for i, month in enumerate(labels):
            x_center = chart_x0 + 18 + i * x_step
            income_height = (incomes[i] / max_value) * chart_height
            expense_height = (expenses[i] / max_value) * chart_height
            income_top = chart_y0 + chart_height - income_height
            expense_top = chart_y0 + chart_height - expense_height

            self.monthly_canvas.create_rectangle(
                x_center - bar_width,
                income_top,
                x_center,
                chart_y0 + chart_height,
                fill="#2e8b57",
                outline="#2e8b57",
                width=1,
            )
            self.monthly_canvas.create_text(x_center - 5, max(income_top - 14, 12), text=f"{incomes[i]:.0f}", fill="#2e8b57", font=(FONT_FAMILY, 8, "bold"))

            self.monthly_canvas.create_rectangle(
                x_center + 8,
                expense_top,
                x_center + bar_width + 8,
                chart_y0 + chart_height,
                fill="#d9534f",
                outline="#d9534f",
                width=1,
            )
            self.monthly_canvas.create_text(x_center + 14, max(expense_top - 14, 12), text=f"{expenses[i]:.0f}", fill="#d9534f", font=(FONT_FAMILY, 8, "bold"))

            self.monthly_canvas.create_text(x_center + 4, chart_y0 + chart_height + 18, text=month[-2:], fill=APP_TEXT, font=(FONT_FAMILY, 11, "bold"))

        self.monthly_canvas.create_text(126, 20, text="   Prihod", fill="#2e8b57", font=(FONT_FAMILY, 13, "bold"))
        self.monthly_canvas.create_rectangle(88, 12, 108, 28, fill="#2e8b57", outline="#2e8b57")
        self.monthly_canvas.create_text(268, 20, text="   Rashod", fill="#d9534f", font=(FONT_FAMILY, 13, "bold"))
        self.monthly_canvas.create_rectangle(226, 12, 246, 28, fill="#d9534f", outline="#d9534f")

    def _draw_pie_chart(self, income, expense):
        self.pie_canvas.delete("all")
        total = income + expense
        if total <= 0:
            self.pie_canvas.create_text(220, 120, text="Nema podataka", fill=APP_TEXT, font=(FONT_FAMILY, 12))
            return

        cx, cy = 150, 110
        radius = 92
        start_angle = 90

        if income > 0:
            income_angle = (income / total) * 360
            self.pie_canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start_angle,
                extent=-income_angle,
                fill="#2e8b57",
                outline=APP_BG,
                width=2,
            )
            start_angle -= income_angle

        if expense > 0:
            expense_angle = (expense / total) * 360
            self.pie_canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start_angle,
                extent=-expense_angle,
                fill="#d9534f",
                outline=APP_BG,
                width=2,
            )

        self.pie_canvas.create_oval(cx - 40, cy - 40, cx + 40, cy + 40, fill=APP_BG, outline=APP_BG)
        self.pie_canvas.create_text(cx, cy, text=f"{(income / total * 100):.0f}%\nPrihod", fill="#2e8b57", font=(FONT_FAMILY, 12, "bold"), justify="center")

        self.pie_canvas.create_rectangle(285, 48, 318, 81, fill="#2e8b57")
        self.pie_canvas.create_text(334, 64, text=f"Prihodi: {income:.2f}", anchor="w", fill=APP_TEXT, font=(FONT_FAMILY, 13, "bold"))

        self.pie_canvas.create_rectangle(285, 92, 318, 125, fill="#d9534f")
        self.pie_canvas.create_text(334, 108, text=f"Rashodi: {expense:.2f}", anchor="w", fill=APP_TEXT, font=(FONT_FAMILY, 13, "bold"))

    def export_csv_report(self):
        file_path = filedialog.asksaveasfilename(
            initialfile="izvestaj_finansija.csv",
            defaultextension=".csv",
            filetypes=[("CSV fajlovi", "*.csv")],
        )
        if not file_path:
            return

        ok = self.controller.finance_service.export_csv(self.controller.current_id, file_path)
        if ok:
            messagebox.showinfo("Uspešno", f"Izveštaj je sačuvan u:\n{file_path}")
        else:
            messagebox.showwarning("Greška", "Nije uspelo exportovanje CSV fajla")

    def export_excel_report(self):
        file_path = filedialog.asksaveasfilename(
            initialfile="izvestaj_finansija.xlsx",
            defaultextension=".xlsx",
            filetypes=[("Excel fajlovi", "*.xlsx")],
        )
        if not file_path:
            return

        ok = self.controller.finance_service.export_excel(self.controller.current_id, file_path)
        if ok:
            messagebox.showinfo("Uspešno", f"Izveštaj je sačuvan u:\n{file_path}")
        else:
            messagebox.showwarning("Greška", "Nije uspelo exportovanje Excel fajla")

    def load_report_data(self):
        transactions = self.controller.finance_service.get_user_transactions(self.controller.current_id) or []

        income = 0.0
        expenses = 0.0
        for transaction in transactions:
            if transaction.amount > 0:
                income += float(transaction.amount)
            else:
                expenses += abs(float(transaction.amount))

        balance = income - expenses

        self._set_card_value("income", self._money(income))
        self._set_card_value("expense", self._money(expenses))
        self._set_card_value("balance", self._money(balance))
        self._set_card_value("count", str(len(transactions)))
        self._draw_pie_chart(income, expenses)

        category_totals = {}
        for transaction in transactions:
            if transaction.amount >= 0:
                continue
            category_key = self._category_name_for_id(transaction.category_id)
            category_totals[category_key] = category_totals.get(category_key, 0.0) + abs(float(transaction.amount))

        for row in self.category_tree.get_children():
            self.category_tree.delete(row)
        for category_name, amount in sorted(category_totals.items(), key=lambda item: item[1], reverse=True):
            self.category_tree.insert("", "end", values=(category_name, f"{amount:.2f}"))

        monthly_data = {}
        for transaction in transactions:
            month = transaction.date[:7] if len(transaction.date) >= 7 else transaction.date
            if month not in monthly_data:
                monthly_data[month] = {"income": 0.0, "expense": 0.0}
            if transaction.amount > 0:
                monthly_data[month]["income"] += float(transaction.amount)
            else:
                monthly_data[month]["expense"] += abs(float(transaction.amount))

        ordered_months = dict(sorted(monthly_data.items(), reverse=True))
        self._draw_monthly_chart(ordered_months)

        for row in self.monthly_tree.get_children():
            self.monthly_tree.delete(row)

        for month in sorted(ordered_months.keys(), reverse=True):
            info = ordered_months[month]
            saldo = info["income"] - info["expense"]
            self.monthly_tree.insert("", "end", values=(month, f"{info['income']:.2f}", f"{info['expense']:.2f}", f"{saldo:.2f}"))

        for row in self.recent_tree.get_children():
            self.recent_tree.delete(row)

        for transaction in sorted(transactions, key=lambda t: t.date, reverse=True)[:8]:
            category_name = self._category_name_for_id(transaction.category_id)
            amount_text = f"{float(transaction.amount):.2f}"
            self.recent_tree.insert(
                "",
                "end",
                values=(transaction.date, category_name, transaction.description or "-", amount_text),
            )

    def _set_card_value(self, key, value):
        if key in self.cards:
            self.cards[key].value_label.config(text=value)
