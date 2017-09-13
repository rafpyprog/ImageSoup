from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import ujson

from . imagesoup import ImageResult


class ReverseSearch():
    def __init__(self):
        self.user_agent = ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/41.0.2228.0 '
                           'Safari/537.36')
        self.driver = None
        self.result_HTML = None
        self.guess = None
        self.similar = None

    def parse_guess(self):
        BEST_GUESS_CLASS = '_gUb'
        guess = self.driver.find_element_by_class_name(BEST_GUESS_CLASS)
        return guess.text

    def parse_similar(self):
        SIMILAR_CLASS = 'iu-card-header'
        similar = self.driver.find_element_by_class_name(SIMILAR_CLASS)
        similar_URL = similar.get_attribute('href')
        self.driver.get(similar_URL)
        IMAGE_CLASS = '.rg_meta.notranslate'
        images = self.driver.find_elements_by_css_selector(IMAGE_CLASS)
        return [i.get_attribute('innerHTML') for i in images]

    def upload_to_google_images(self, filepath):
        BASE_URL = 'https://www.google.com/searchbyimage/upload'
        multipart = {'encoded_image': (filepath, open(filepath, 'rb')),
                     'image_content': ''}

        headers = {'User-Agent': self.user_agent,
                   'origin': 'https://www.google.com',
                   'referer': 'https://www.google.com/'}

        response = requests.post(BASE_URL, files=multipart, headers=headers,
                                 allow_redirects=False)

        result_URL = response.headers['Location']
        return result_URL

    def search(self, filepath, language='en'):
        if not self.driver:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = Chrome(chrome_options=chrome_options)

        search_result_URL = self.upload_to_google_images(filepath)
        self.driver.get(search_result_URL + '&hl={}'.format(language))

        self.result_HTML = self.driver.page_source
        self.guess = self.parse_guess()
        self.similar = self.parse_similar()
        return None






'''
soup_rev = ReverseSearch()
filepath = 'D:\\Projetos\\#DEV Python\\ImageSoup\\imagesoup\\MG.png'
soup_rev.search(filepath)
soup_rev.guess

l = soup_rev.similar'''
