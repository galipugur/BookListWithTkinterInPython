import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.webdriver.support import expected_conditions
import os
import requests
from io import BytesIO
from PIL import Image
from unidecode import unidecode
import random
from tkinter import messagebox

class KitapCrawler:
    def __init__(self):
        self.url = "https://1000kitap.com/kitaplar/en-cok-okunanlar?hl=tr"
        self.download_image_count = 0
        # self.driver = webdriver.Chrome()

    def create_folder(self, folder_path):
        try:
            os.makedirs(folder_path, exist_ok=True)
        except FileExistsError:
            pass

    def write_to_csv(self, data_list):
        basliklar = ["ID", "book_name", "author", "like_and_read", "book_id"]
        folder_path = 'data'
        self.create_folder(folder_path)
        file_path = os.path.join(folder_path, 'kitap.csv')
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerow(basliklar)
            for item in data_list:
                writer.writerow(item)
        print(f'CSV dosyası oluşturuldu. {len(data_list)} adet kitap vardır.')
        print(f"{self.download_image_count} tane resim vardır.")

    def is_page_loaded(self):
        return self.driver.execute_script("return document.readyState === 'complete'")

    def navigate_to_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    def get_total_pages(self):
        try:
            scroll_down = (self.driver.find_element
                           (By.XPATH, "/html/body/div[1]/div/div/div[2]/div/section/div[20]/div[1]/a[2]/span"))
        except:
            return self.get_total_pages()

        self.scroll_to_element(scroll_down)
        page_count = int(scroll_down.text)
        return page_count

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_next_page_button(self):
        try:
            cookie_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/button")
            cookie_button.click()
        except:
            pass

        try:
            scroll_down = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/section/div[20]/div[1]")
            self.scroll_to_element(scroll_down)
            a_count = len(self.driver.find_element
                          (By.XPATH, "/html/body/div[1]/div/div/div[2]/div/section/div[20]/div[1]")
                          .find_elements(By.TAG_NAME, "a"))
            next_page_button = (self.driver.find_element
                                (By.XPATH, f"/html/body/div[1]/div/div/div[2]/div/section/div[20]/div[1]/a[{a_count}]"))
            next_page_button.click()
        except:
            pass

    def get_book_information(self):
        self.navigate_to_url(self.url)
        total_pages = self.get_total_pages()
        book_list = []

        for page in range(total_pages):
            time.sleep(10)
            if len(book_list) <= 120:
                div_count = int(len(self.driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/section/div")))
                for i in range(div_count):
                    WebDriverWait(self.driver, 30).until(lambda driver: self.is_page_loaded())
                    data_type = self.driver.find_element(By.XPATH,
                                                          f"/html/body/div[1]/div/div/div[2]/div/section/div[{i + 1}]").get_attribute(
                        "data-turu")
                    if data_type == "kitap":
                        order = (self.driver.find_element
                            (By.XPATH,f"/html/body/div[1]/div/div/div[2]/div/section/div[{i + 1}]/div/div[1]/span").text)
                        book_name = (self.driver.find_element
                            (By.XPATH,f"/html/body/div[1]/div/div/div[2]/div/section/div[{i + 1}]/div/div[2]/div/div[1]/a/h3").text)
                        author = (self.driver.find_element
                            (By.XPATH,f"/html/body/div[1]/div/div/div[2]/div/section/div[{i + 1}]/div/div[2]/div/div[1]/div[1]/a").text)
                        like_read = (self.driver.find_element
                            (By.XPATH,f"/html/body/div[1]/div/div/div[2]/div/section/div[{i + 1}]/div/div[2]/div/div[1]/div[2]/span/span").text.strip())
                        book_id = self.img_id()
                        self.get_book_image(for_image=book_id, key=i + 1)
                        book_list.append((order, book_name, author, like_read, book_id))
                self.click_next_page_button()
            else:
                break

        return book_list

    def img_id(self):
        id_list = []
        image_id = random.randint(1000, 10000)
        if not image_id in id_list:
            id_list.append(image_id)
        else:
            self.img_id()

        return image_id

    def get_book_image(self, for_image, key):
        self.download_image_count += 1
        folder_path = 'images'
        self.create_folder(folder_path)

        image_element = (self.driver.find_element
                         (By.CSS_SELECTOR,
                          f"#__next > div > div > div.dr.flex-1.flex-column.items-center > div > section > div:nth-child({key}) > div > a > div > img"))
        image_url = image_element.get_attribute('src')
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image.resize((40, 60))
        image.save(os.path.join(f"{folder_path}/{for_image}.jpg"))

    def main(self):
        user_confirmation = messagebox.askyesno("Onay", "Kitapları çekmek istediğinize emin misiniz?")
        if not user_confirmation:
            print("İşlem iptal edildi.")
            exit()

        self.driver = webdriver.Chrome()
        try:
            book_list = self.get_book_information()
            self.write_to_csv(data_list=book_list)
        finally:
            if self.driver is not None:
                self.driver.quit()

if __name__ == "__main__":
    kitap_crawler = KitapCrawler()
    try:
        kitap_crawler.main()
    finally:
        if kitap_crawler.driver is not None:
            kitap_crawler.driver.quit()
