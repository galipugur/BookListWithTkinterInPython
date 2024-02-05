"""Kitapların olduğu listeyi içerir."""
import csv, math
import tkinter as tk
from tkinter import ttk
from data.renkler import RENKLER
from PIL import Image, ImageTk
from sayfalar.kitap_detayi.KitapDetayi import KitapDetayi

class KitapListesi:
    """Kitap Listesi Frame i"""

    sutunlar = ['book_id', 'ID', "book_name", "author"]
    sayfa_no = 1
    sayfa_basina_adet = 6
    toplam_sayfa_sayisi = 0

    def __init__(self, master, fon_rengi, relief=tk.SUNKEN, side=tk.LEFT):
        self.frame = tk.Frame(
            master=master,
            name='kitapListesi',
            bg=fon_rengi,
            relief=relief,
        )
        self.side = side
        self.kitaplar = []
        self.add_to_frame()
        self.create_to_page()


    def add_to_frame(self):
        self.frame_title('Kitap Listesi')
        self.read_to_csv()
        # self.create_to_page()
        self.frame.pack(side=self.side, fill=tk.BOTH, expand=True)

    def frame_title(self, baslik):
        title = tk.Label(
            master=self.frame, text=baslik, bg=RENKLER.SIYAH,
            fg=RENKLER.BEYAZ, font=('Arial', 10, 'bold'), height=3
        )
        title.grid(row=0, column=0, columnspan=6, padx=1, pady=(0, 8), sticky='we') # sticky='we' --> batı ve doğuya yasla demek)


    def read_to_csv(self):
        read_to_book = "data/kitap.csv"
        with open(read_to_book, 'r', encoding='utf-8') as books:
            book_dict = csv.DictReader(books, delimiter=',')
            for book in book_dict:
                self.kitaplar.append(book)

        KitapListesi.toplam_sayfa_sayisi = math.ceil(len(self.kitaplar) / KitapListesi.sayfa_basina_adet + 1)

    def create_to_page(self):
        self.add_title_row()
        self.tablo_olustur()
        self.combobox_olustur()

    def add_title_row(self):
        for i, sutun in enumerate(KitapListesi.sutunlar):
            if sutun != "book_id":
                lbl = tk.Label(
                    master=self.frame, text=str(sutun), height=2,
                    width=30, bg=RENKLER.SIYAH, fg=RENKLER.BEYAZ,
                    font=('Arial', 9, 'bold')
                )

                if sutun == 'ID':
                    lbl.config(text='#', width=4)
                elif sutun == 'book_name':
                    lbl.config(text='Kitap Adı')
                elif sutun == 'author':
                    lbl.config(text='Yazar')

                if sutun == 'author':
                    lbl.grid(row=1, column=i, sticky='we', padx=(0, 10))
                else:
                    lbl.grid(row=1, column=i, sticky='we', padx=(0, 1))


    def tablo_olustur(self):
        for i, book in enumerate(self.kitaplar):
            if (KitapListesi.sayfa_no - 1) * (
                    KitapListesi.sayfa_basina_adet) <= i < KitapListesi.sayfa_no * KitapListesi.sayfa_basina_adet:
                for j, key in enumerate(KitapListesi.sutunlar):
                    name = 'table_row_' + str(i) + str(j) + '_' + book['book_id']
                    if j == 0:
                        # resim bas
                        self.render_image(book, i, j, name)
                    else:
                        # pass
                        # yazı yaz. film bilgisi
                        self.write_label(book, i, j, key, name)
            self.i = i + 3

    def render_image(self, book, i, j, name):
        try:
            # resim var mı bak
            load = Image.open("images/" + book['book_id'] + ".jpg")
            base_width = 40
            wpercent = (base_width / float(load.size[0]))
            hsize = int((float(load.size[1]) * float(wpercent)))
            load = load.resize((base_width, hsize), Image.Resampling.LANCZOS)
        except:
            # yoksa noimage
            load = Image.open("images/python_icon.png")
        finally:
            render = ImageTk.PhotoImage(load)
            img_label = tk.Label(self.frame, name=name, image=render, bg='orange')
            img_label.image = render
            img_label.grid(row=i + 2, column=j, padx=(7, 0), sticky='we')

    def write_label(self, book, i, j, key, name):
        lbl = tk.Label(self.frame, name=name, text=str(book[key]),
                       height=4, fg='black', font=('Arial', 10, 'bold'),
                       cursor='hand2')
        lbl.bind('<Button-1>', self.film_click)
        if key == 'ID':
            lbl.config(width=4)
        elif key == 'book_name':
            lbl.config(width=31, anchor='w')
        elif key == 'author':
            lbl.config(width=12, anchor='w')

        self.fill_bg(lbl, i)

        if key == 'author':
            lbl.grid(row=i + 2, column=j, sticky='we', padx=(0, 10))
        else:
            lbl.grid(row=i + 2, column=j, sticky='we', padx=(0, 1))


    def fill_bg(self, widget, i):
        if i % 2 == 1:
            widget.config(bg=RENKLER.LIST_SATIR_TEK)
        else:
            widget.config(bg=RENKLER.LIST_SATIR_CIFT)

    def combobox_olustur(self):
        values = list(range(1, KitapListesi.toplam_sayfa_sayisi))
        sayfalar = ttk.Combobox(self.frame, width=4, values=values)
        sayfalar.current(KitapListesi.sayfa_no - 1)
        sayfalar.bind('<<ComboboxSelected>>', self.combobox_selected_event)
        sayfalar.place(x=300, y=550)
        # sayfalar.grid(row=self.i, column=2, pady=(15, 0))

    def combobox_selected_event(self, event):
        KitapListesi.sayfa_no = int(event.widget.get())  # kullanıcının seçtiği indexi verir.
        self.tablo_bosalt(event)
        self.tablo_olustur()

    def tablo_bosalt(self, event):
        master = event.widget.master
        for child in master.children.copy():
            if 'table_row' in child:
                master.children[child].destroy()

    def film_click(self, event):
        book_id = str(event.widget).split('_')[3]

        # önce sağ frame içini düzenle
        self.sag_frame_duzenle(event, book_id)

        # sol frame düzenle
        self.sol_frame_duzenle(event)

    def sol_frame_duzenle(self, event):
        root = event.widget.master.master.master # en tepeye çıkmış oluyoruz.
        for child in root.winfo_children():
            if str(child) == '.solFrame':
                for ch in child.winfo_children():
                    if str(ch) == '.solFrame.kitapDetayi':
                        ch.config(bg=RENKLER.TURUNCU, fg=RENKLER.BEYAZ)
                    else:
                        ch.config(bg=RENKLER.SIYAH, fg=RENKLER.TURUNCU)

    def sag_frame_duzenle(self, event, bookId):
        sgFrame = event.widget.master
        for child in sgFrame.winfo_children():
            child.destroy()

        # film detay sayfasını yaz.
        KitapDetayi(sgFrame, 'orange', bookId=bookId, kitaplar=self.kitaplar)


        
