import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from . imagesoup import ImageResult, ImageSoup


class ReverseSearchResult():
    def __init__(self, HTML):
        self.HTML = HTML
        self.soup = BeautifulSoup(self.HTML, 'lxml')
        self._label = None
        self._similar_images = None

    @property
    def label(self):
        if self._label is None:
            self._label = self.parse_image_label()
        return self._label

    @property
    def similar_images(self):
        if self._similar_images is None:
            self._similar_images = self.parse_similar_images()
        return self._similar_images

    def parse_image_label(self):
        card = self.soup.find('div', {'class': 'card-section'})
        best_guess_text = card.find_all('a')[-1].text
        return best_guess_text

    def parse_similar_images(self):
        similar_images_a_tag = self.soup.find('a', {'class': 'iu-card-header'})
        google_domain = 'http://www.google.com/'
        similar_images_url = urljoin(google_domain,
                                     similar_images_a_tag['href'])
        image_soup = ImageSoup()
        result_HTML = image_soup.get_search_result_page(similar_images_url)
        images_data = image_soup.get_images_data_from_HTML(result_HTML)
        similar_images = image_soup.get_images_results(images_data)
        print(similar_images)
        return similar_images


class ReverseSearch():
    def __init__(self):
        self.user_agent = ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/41.0.2228.0 '
                           'Safari/537.36')

    def search(self, filepath):
        HTML = self.post_image_search_on_google(filepath)
        return ReverseSearchResult(HTML)

    def post_image_search_on_google(self, filepath):
        search_url = 'http://www.google.com/searchbyimage/upload'
        multipart = {'encoded_image': (filepath, open(filepath, 'rb')),
                     'image_content': ''}
        session = requests.Session()
        post_search = session.post(search_url, files=multipart,
                                   allow_redirects=False)
        search_response_url = post_search.headers['Location']
        search_result = session.get(search_response_url, allow_redirects=False)
        search_result_URL = search_result.headers['Location']

        headers = {'User-Agent': self.user_agent}
        result_HTML = session.get(search_result_URL, headers=headers).text
        return result_HTML
