"""Sağ taraf bilgileri"""

import tkinter as tk
from data.renkler import RENKLER
from sayfalar import AnaSayfa, KitapListesi, KitapDetayi

class SagFrame:
    def __init__(self, window, name, relief=tk.SUNKEN, side=tk.LEFT):
        self.frame = tk.Frame(
            master=window, name=name,
            relief=relief, bg=RENKLER.TURUNCU
        )
        self.side = side
        self.add_to_frame()

    def add_to_frame(self):
        self.frame_content()
        self.frame.pack(side=self.side, fill=tk.BOTH, expand=True)

    def frame_content(self, sayfa_adi='anaSayfa'):
        try:
            gelenFrame = self.frame
        except:
            gelenFrame = self
        finally:
            if sayfa_adi == 'anaSayfa':
                # ana sayfayı çağır
                AnaSayfa(gelenFrame, fon_rengi=RENKLER.TURUNCU)
            elif sayfa_adi == 'kitapListesi':
                # kitap listesini çağır
                pass
                KitapListesi(gelenFrame, RENKLER.TURUNCU)
            elif sayfa_adi == 'kitapDetayi':
                # kitap detay sayfası
                KitapDetayi(gelenFrame, RENKLER.TURUNCU)

    def destroy_children(frame):
        # frame içindeki tüm birimleri (çocukları) sil
        for child in frame.winfo_children():
            child.destroy()