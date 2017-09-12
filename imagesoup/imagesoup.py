import io
import json
import math

from PIL import Image
from bs4 import BeautifulSoup
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from . import colors
from . import parameters

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
        except (IOError, OSError):
            print('Cannot identify image file from {}'.format(self.URL))
            return False
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
        ratio = float(new_height) / self.height
        width = math.ceil(self.width * ratio)
        height = math.ceil(self.height * ratio)
        size = (int(width), int(height))

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
        self.user_agent = ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/41.0.2228.0 '
                           'Safari/537.36')

    def get_search_result_page(self, URL):
        headers = {'User-Agent': self.user_agent}
        response = requests.get(URL, headers=headers)
        if response.status_code != 200:
            error_msg = 'Error on search request - HTTP {}. Expected 200'
            raise(error_msg.format(response.status_code))
        search_result_HTML = response.text
        return search_result_HTML

    def get_images_data_from_HTML(self, HTML):
        soup = BeautifulSoup(HTML, 'html.parser')

        divs = soup.findAll('div')
        divs_has_class = list(filter(lambda x: x.has_attr('class'), divs))

        IMAGE_CLASS = ['rg_meta', 'notranslate']
        images_data = filter(lambda x: x['class'] == IMAGE_CLASS,
                             divs_has_class)
        return list(images_data)

    def get_images_results(self, images_data):
        results = []
        for image in images_data:
            URL = json.loads(image.text)['ou']
            results.append(ImageResult(URL))
        return results

    def search(self, query, image_size=None, aspect_ratio=None, n_images=100):
        FIRST_SEARCH_RESULT_PAGE = 0
        RESULTS_PER_PAGE = 100  # Returned by Google Images

        LAST_SEARCH_RESULT_PAGE = math.ceil(float(n_images) / RESULTS_PER_PAGE)

        images_results = []
        for page_number in range(FIRST_SEARCH_RESULT_PAGE,
                                 int(LAST_SEARCH_RESULT_PAGE)):
            URL = parameters.query_builder(query, image_size, aspect_ratio,
                                           page_number)
            HTML = self.get_search_result_page(URL)
            images_data = self.get_images_data_from_HTML(HTML)
            if len(images_data) == 0:  # end of results. stop interating
                msg = 'Search query "{}" returned only {} images.'
                print(msg.format(query, len(images_results)))
                break
            images_results.extend(self.get_images_results(images_data))
        search_result = images_results[:n_images]
        return search_result
