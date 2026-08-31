import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

FONT_FAMILY = "Courier New"

FONT_SMALL = (FONT_FAMILY, 12)
FONT_MEDIUM = (FONT_FAMILY, 16)
FONT_LARGE = (FONT_FAMILY, 28, "bold")

APP_BG = "#f3f3f3"
APP_PANEL = "#e7e7e7"
APP_TEXT = "#1f1f1f"
APP_MUTED = "#5b5b5b"
APP_ACCENT = "#d9d9d9"


def apply_global_theme(root):
    root.configure(bg=APP_BG)

    style = ttk.Style(root)
    style.configure(".", background=APP_BG, foreground=APP_TEXT, font=FONT_MEDIUM)
    style.configure("TFrame", background=APP_BG)
    style.configure("TNotebook", background=APP_BG)
    style.configure("TNotebook.Tab", background=APP_PANEL, foreground=APP_TEXT, padding=(12, 6))
    style.map("TNotebook.Tab", background=[("selected", APP_BG), ("active", APP_ACCENT)])
    style.configure("TLabelframe", background=APP_BG)
    style.configure("TLabelframe.Label", background=APP_BG, foreground=APP_TEXT, font=FONT_MEDIUM)
    style.configure("TLabel", background=APP_BG, foreground=APP_TEXT, font=FONT_MEDIUM)
    style.configure("TButton", background=APP_PANEL, foreground=APP_TEXT, font=FONT_MEDIUM)
    style.map("TButton", background=[("active", APP_ACCENT), ("pressed", APP_ACCENT)])
    style.configure("TEntry", fieldbackground="#ffffff", foreground=APP_TEXT, font=FONT_MEDIUM)
    style.configure("TCombobox", fieldbackground="#ffffff", foreground=APP_TEXT, font=FONT_MEDIUM)
    style.configure("TRadiobutton", background=APP_BG, foreground=APP_TEXT, font=FONT_MEDIUM)
    style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground=APP_TEXT, font=FONT_MEDIUM, rowheight=28)
    style.configure("Treeview.Heading", background=APP_PANEL, foreground=APP_TEXT, font=FONT_MEDIUM)

    return root


def apply_popup_theme(window):
    apply_global_theme(window)

    for child in window.winfo_children():
        if isinstance(child, tk.Widget):
            try:
                child.configure(bg=APP_BG)
            except Exception:
                pass

    return window