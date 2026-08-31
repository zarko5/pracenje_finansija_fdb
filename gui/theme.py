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


def apply_popup_theme(window):
    window.configure(bg=APP_BG)

    style = ttk.Style(window)
    style.configure("TFrame", background=APP_BG)
    style.configure("TLabel", background=APP_BG, foreground=APP_TEXT)
    style.configure("TButton", background=APP_PANEL, foreground=APP_TEXT)
    style.configure("TEntry", fieldbackground="#ffffff", foreground=APP_TEXT)
    style.configure("TCombobox", fieldbackground="#ffffff", foreground=APP_TEXT)
    style.configure("TRadiobutton", background=APP_BG, foreground=APP_TEXT)
    style.map("TButton", background=[("active", APP_ACCENT)])

    for child in window.winfo_children():
        if isinstance(child, tk.Widget):
            try:
                child.configure(bg=APP_BG)
            except Exception:
                pass

    return window