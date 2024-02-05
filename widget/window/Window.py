"""anasayfa ekranı"""

import tkinter as tk
from data.renkler import RENKLER
from data.geometri import GEOMETRI


class Window:
    def __init__(self, title):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.config(bg=RENKLER.SIYAH)
        self.boyut_ayarla()

    def boyut_ayarla(self):
        w, h = (GEOMETRI.ANA_SAYFA_GENISLIK, GEOMETRI.ANA_SAYFA_YUKSEKLIK)
        return self.window.geometry(f"{w}x{h}")

    def start_window(self):
        self.window.mainloop()