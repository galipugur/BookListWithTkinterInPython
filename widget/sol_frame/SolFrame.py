"""
Sol taraf bilgilerini tutacak
1- Anasayfa
2- Kitap Listesi
3- Kitap Detay
"""

import tkinter as tk
from data.renkler import RENKLER
from data.menuler import MENU
from widget.button.Button import Button
from widget.sag_frame.SagFrame import SagFrame


class SolFrame:
    def __init__(self, window, name):
        self.frame = tk.Frame(
            master=window,
            name=name,
            bg=RENKLER.SIYAH,
        )
        self.master = window
        self.add_to_frame()
        self.add_to_menu()

    def add_to_frame(self):
        self.frame.pack(side=tk.LEFT, fill=tk.Y, pady=(30, 0))

    def add_to_menu(self):
        for menu_key, menu_text in MENU.items():
            if menu_key == "uygulamaHakkinda":
                button = Button(
                    master=self.frame, name=menu_key, text=menu_text,
                    bg=RENKLER.SIYAH, fg=RENKLER.BEYAZ, en=15, boy=2,
                    side=tk.BOTTOM, handle_click=self.handle_click
                )
            else:
                button = Button(
                    master=self.frame, name=menu_key, text=menu_text,
                    bg=RENKLER.SIYAH, fg=RENKLER.BEYAZ, en=15, boy=2,
                    handle_click=self.handle_click
                )

                if menu_key == 'anaSayfa':
                    SolFrame.secili_button_rengi(button.button)

    def button_renklerini_yonet(self, event):
        #tıklanan buton: event.widget
        # seçili olan ve tüm kardeşlerini siyah yap.
        for child in event.widget.master.winfo_children():
            child.config(bg=RENKLER.SIYAH, fg=RENKLER.TURUNCU)
        # seçili olanı turuncu yap.
        SolFrame.secili_button_rengi(event.widget)

    def handle_click(self, event):
        self.button_renklerini_yonet(event)

        # tıkladığımız butonun ismini almak için bunu yapıyoruz.
        sayfa_adi = str(event.widget).split('.')[2]
        # print(sayfa_adi)

        # sagFrame al
        sgFrame = self.master.children['sagFrame']

        # sagFrame içindeki children olanları yani içinde ne varsa destroy et.
        SagFrame.destroy_children(sgFrame)

        # üstte sağ tarafın içeriğini temizledik.
        # şimdi elimizde hazır isim varken onu kullanarak içerik oluşturacağız.
        SagFrame.frame_content(sgFrame, sayfa_adi)



    def secili_button_rengi(button):
        button.config(bg=RENKLER.TURUNCU, fg=RENKLER.BEYAZ)
