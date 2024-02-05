"""Ana sayfa içeriğini burada görüntüleyebilirsiniz."""

import tkinter as tk
from PIL import Image, ImageTk

class AnaSayfa:
    def __init__(self, window, fon_rengi, relief=tk.SUNKEN, side=tk.LEFT):
        self.frame = tk.Frame(
            master=window,
            bg=fon_rengi,
            name='anaSayfa',
            relief=relief
        )
        self.side = side
        self.add_to_frame()
        self.frame_content()


    def add_to_frame(self):
        self.frame.pack(side=self.side, fill=tk.BOTH, expand=True)

    def frame_content(self):
        tanitim = tk.Label(master=self.frame,
                           text='Temel Python',
                           font=('Helvatica', 16, 'bold'),
                           bg='orange', fg='white')
        tanitim.place(x=206, y=5)

        isim = (tk.Label(self.frame,
                         text='(Galip UĞUR)',
                         font=('Helvatica', 16, 'bold'),
                         bg='orange', fg='white'))
        isim.place(x=210, y=45)

        self.render_image()

        proje = tk.Label(self.frame,
                         text='Bu Python Kursu Bitirme Projesidir',
                         font=('Helvatica', 15, 'bold'),
                         bg='black', fg='white')
        proje.place(x=110, y=520)

    def render_image(self):
        load = Image.open('python_icon.png')
        render = ImageTk.PhotoImage(load)
        img_lbl = tk.Label(master=self.frame, image=render, bg='orange')
        img_lbl.image = render
        img_lbl.place(x=155, y=160)
