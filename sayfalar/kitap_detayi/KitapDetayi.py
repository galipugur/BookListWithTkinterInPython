import tkinter as tk
from data.renkler import RENKLER
from PIL import Image, ImageTk


class KitapDetayi:
    """Kitapların detayları"""

    def __init__(self, window, fon_rengi, bookId=None, kitaplar=[], relief=tk.SUNKEN, side=tk.LEFT):
        self.frame = tk.Frame(
            master=window,
            name='kitapDetayi',
            relief=relief,
            bg=fon_rengi
        )
        self.side = side
        self.bookId = bookId
        self.kitaplar = kitaplar
        self.add_to_frame()

    def add_to_frame(self):
        self.frame_content()
        self.frame_title("Kitap Detayı")
        self.frame.pack(side=self.side, fill=tk.BOTH, expand=True)

    def frame_title(self, baslik):
        if self.bookId != None:
            title = tk.Label(
                master=self.frame, text=self.kitap['book_name'], bg=RENKLER.SIYAH,
                fg=RENKLER.BEYAZ, font=('Arial', 10, 'bold'), height=3
            )
            title.grid(row=0, column=0, columnspan=6, padx=1, pady=(0, 8), sticky='we')
        else:
            title = tk.Label(
                master=self.frame, text=baslik, bg=RENKLER.SIYAH,
                fg=RENKLER.BEYAZ, font=('Arial', 10, 'bold'), height=3
            )
            title.pack(fill=tk.X, padx=(1, 0))

    def frame_content(self):
        if self.bookId != None:
            self.render_image()
            self.get_film()
            self.render_keys()
            self.render_value()
        else:
            pass

    def render_image(self):
        try:
            # resim var mı bak
            load = Image.open("images/" + str(self.bookId) + ".jpg")
            base_width = 140
            wpercent = (base_width / float(load.size[0]))
            hsize = int((float(load.size[1]) * float(wpercent)))
            load = load.resize((base_width, hsize), Image.Resampling.LANCZOS)
        except:
            # yoksa noimage
            load = Image.open("images/python_icon.png")
        finally:
            render = ImageTk.PhotoImage(load)
            img_label = tk.Label(self.frame, image=render, bg='orange')
            img_label.image = render
            img_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

    def get_film(self):
        for k in self.kitaplar:
            if k['book_id'] == self.bookId:
                self.kitap = k
                break

    def render_keys(self):
        for i, key in enumerate(self.kitap.keys()):
            txt = str(key)
            lbl = tk.Label(master=self.frame, text=txt, height=2, width=16, anchor='w')
            self.fill_bg(lbl, i)
            lbl.grid(row=i + 2, column=0, padx=(10, 1))

    def render_value(self):
        for i, value in enumerate(self.kitap.values()):
            txt = str(value)
            lbl = tk.Label(master=self.frame, text=txt, height=2, width=60, anchor='w')
            self.fill_bg(lbl, i)
            lbl.grid(row=i + 2, column=1, padx=(0, 8))

    def fill_bg(self, widget, i):
        if i % 2 == 1:
            widget.config(bg=RENKLER.LIST_SATIR_TEK)
        else:
            widget.config(bg=RENKLER.LIST_SATIR_CIFT)