import os
import io
import json
import math

from PIL import Image, ImageFile
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import colors

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ImageResult():
    def __init__(self, URL):
        self.URL = URL
        self.is_downloaded = False
        self.response = None
        self.verify_SSL = False

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.URL)

    def _download(self):
        self.response = requests.get(self.URL, verify=self.verify_SSL)
        self.response.raise_for_status()
        self.is_downloaded = True

    def to_file(self, filepath=None):
        if not filepath:
            filepath = '{}.{}'.format('image', self.format)
        with open(filepath, 'wb') as f:
            f.write(self.content.getvalue())

    def verify(self):
        try:
            self._im.load()
        except OSError as e:
            print('Cannot identify image file from {}'.format(self.URL))
        else:
            return True

    def getcolors(self):
        return self._im.getcolors(self.width * self.height)

    def resize(self, size):
        im = self._im.resize(size)
        return im

    @property
    def content(self):
        if not self.is_downloaded:
            self._download()
        return io.BytesIO(self.response.content)

    @property
    def color_count(self):
        return len(self.getcolors())

    @property
    def _im(self):
        return Image.open(self.content)

    @property
    def format(self):
        return self._im.format.lower()

    @property
    def width(self):
        return self._im.width

    @property
    def height(self):
        return self._im.height

    @property
    def size(self):
        return self._im.size

    @property
    def info(self):
        return self._im.info

    @property
    def dpi(self):
        return self.info.get('dpi', None)

    @property
    def mode(self):
        return self._im.mode

    def show(self):
        self._im.show()

    def convert(self, mode):
        ''' Returns a converted copy of the image '''
        return self._im.convert(mode)

    def reduce(self, new_height=100):
        ''' Reduce an image to a new_height keeping proportions '''
        ratio = new_height / self.height
        size = int(self.width * ratio), int(self.height * ratio)
        im = self._im.resize(size)
        return im

    def main_color(self, n=1, reduce_size=False, height=100):
        im = self._im
        if reduce_size:
            im = self.reduce(new_height=height)
        color_counter = colors.color_analysis(im)
        return color_counter.most_common(n)


class ImageSoup():
    def __init__(self):
        self.user_agent = self.user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

    def get_search_result_page(self, query, page_number=0):
        headers = {'User-Agent': self.user_agent}
        google_images = 'https://www.google.com/search?q={}&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg&ijn={}'
        response = requests.get(google_images.format(query, page_number),
                                headers=headers)
        if response.status_code != 200:
            raise('Error on search request - HTTP {}. Expected 200'.format(response.status_code))
        search_result_HTML = response.text
        return search_result_HTML

    def get_images_data_from_HTML(self, HTML):
        soup = BeautifulSoup(HTML, 'html.parser')
        divs_has_class = [div for div in soup.findAll("div") if div.has_attr('class') == True]
        images_data = [div for div in divs_has_class if div['class'] == ['rg_meta', 'notranslate']]
        return images_data

    def get_images_results(self, images_data):
        results = []
        for image in images_data:
            URL = json.loads(image.text)['ou']
            results.append(ImageResult(URL))
        return results

    def search(self, query, n_images=100):
        FIRST_SEARCH_RESULT_PAGE = 0
        RESULTS_PER_PAGE = 100  # Returned by Google Images
        LAST_SEARCH_RESULT_PAGE = math.ceil(n_images / RESULTS_PER_PAGE)

        images_results = []
        for page_number in range(FIRST_SEARCH_RESULT_PAGE, LAST_SEARCH_RESULT_PAGE):
            HTML = self.get_search_result_page(query, page_number)
            images_data = self.get_images_data_from_HTML(HTML)
            if len(images_data) == 0:  # end of results. stop interating
                msg = 'Search query "{}" returned only {} images.'
                print(msg.format(query, len(images_results)))
                end_page = page_number
                break
            images_results.extend(self.get_images_results(images_data))
            end_page = page_number + 1
        search_result = images_results[:n_images]
        return search_result
