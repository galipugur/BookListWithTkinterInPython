"""
Kitaplık Uygulaması (From Tkinter)
1- Anasayfa
2- Kitap Listesi
3- Kitap Detay
"""

from widget import Window, SolFrame, SagFrame
from webden_gelenler import KitapCrawler
import os

klasor_yolu = os.getcwd()
csv_dosyasi = os.path.join(klasor_yolu, 'data\kitap.csv')
img_klasoru = os.path.join(klasor_yolu, 'images')

if __name__ == "__main__":

    if not os.path.exists(csv_dosyasi) or not os.path.exists(img_klasoru):
        kitap_crawler = KitapCrawler()
        kitap_crawler.main()

    # anasayfa
    app_window = Window("MY LİBRARY")

    # SolFrame
    left_frame = SolFrame(app_window.window, "solFrame")

    # SagFrame
    right_frame = SagFrame(app_window.window, name="sagFrame")

    # uygulama baslat(loop)
    app_window.start_window()