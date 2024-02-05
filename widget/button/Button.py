"""Butonları içeren dosya"""

import tkinter as tk
from data.renkler import RENKLER

class Button:
    def __init__(self, master, name, text,
                 fg, bg, en, boy, handle_click,
                 padx=0, pady=0, side=tk.TOP):
        self.button = tk.Button(
            master=master, name=name, text=text,
            width=en, height=boy, bg=bg, fg=fg,
            activebackground=RENKLER.ANTRASIT1
        )
        self.padx = padx
        self.pady = pady
        self.side = side
        self.button_ekle()
        self.event_bagla(handle_click=handle_click)

    def button_ekle(self):
        self.button.config(font=('Arial', 10))
        self.button.pack(
            padx=self.padx,
            pady=self.pady,
            side=self.side
        )

    def event_bagla(self, handle_click):
        # '<Button-1>' --->> mouse ile sol tık eventi
        self.button.bind('<Button-1>', handle_click)