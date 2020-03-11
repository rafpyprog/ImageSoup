import os
import pytest


from bs4 import BeautifulSoup
from imagesoup import ImageSoup, ImageResult, parameters
from imagesoup.utils import Blacklist
from imagesoup.reverse_search import *


SEARCH_QUERY = "python"


def test_creating_soup():
    assert isinstance(ImageSoup(), ImageSoup)


def test_get_search_result_page():
    EXPECTED_PAGE_TITLE = f"{SEARCH_QUERY} - Google Search"

    url = parameters.query_builder(SEARCH_QUERY)
    html = ImageSoup().get_search_result_page(url)

    assert isinstance(html, str)
    assert BeautifulSoup(html, features="html.parser").title.text == EXPECTED_PAGE_TITLE


def test_get_results_data_id_from_html():
    url = parameters.query_builder(SEARCH_QUERY)
    soup = ImageSoup()
    html = soup.get_search_result_page(url)
    images_data = soup.get_results_data_id_from_HTML(html)
    assert isinstance(images_data, list)
    assert len(images_data) == 20


def test_get_image_results():
    url = parameters.query_builder(SEARCH_QUERY)

    soup = ImageSoup()
    html = soup.get_search_result_page(url)
    images_data = soup.get_results_data_id_from_HTML(html)

    image_results = soup.get_images_results(images_data)

    assert isinstance(image_results, list)
    assert all(isinstance(i, ImageResult) for i in image_results)
    assert len(image_results) == 20


def test_search_query_only_returns_100_images():
    soup = ImageSoup()
    images = soup.search('python')
    assert len(images) == 100
    assert all(isinstance(img, ImageResult) for img in images)


def test_search_n_images_set_by_user():
    N_IMAGES = 20
    soup = ImageSoup()
    images = soup.search('python', n_images=N_IMAGES)
    assert len(images) == N_IMAGES



def test_search_with_image_size_parameter():
    soup = ImageSoup()
    images = soup.search('python site:python.org', image_size='large')
    im = images[0]
    width, height = im.size
    assert width > 500 and height > 500


def test_search_image_exact_size():
    soup = ImageSoup()
    size = (400, 400)
    images = soup.search('python', image_size=size)
    im = images[0]
    assert im.size == size


def test_search_image_aspect_ratio():
    soup = ImageSoup()
    images = soup.search('python site:python.org', aspect_ratio='tall')
    im = images[0]
    assert im.height > im.width


def test_search_image_returns_fewer_results_than_n_images(capsys):
    soup = ImageSoup()
    images = soup.search('python', n_images=2000)
    out, err = capsys.readouterr()
    assert out.startswith('Search query "python" returned only')


def test_imageresult_url():
    soup = ImageSoup()
    images = soup.search('python site:python.org')
    im = images[0]
    assert im.URL.startswith('http')


def test_imageresult_show_image():
    soup = ImageSoup()
    images = soup.search('python logo png')
    try:
        images[0].show()
    except:
        pytest.fail('Cant show image')


def test_imageresult_resize():
    soup = ImageSoup()
    images = soup.search('python logo PNG')
    im = images[0]
    new_size = (400, 400)
    new_image = im.resize(new_size)
    assert new_image.size == new_size


def test_get_image_main_color():
    soup = ImageSoup()
    images = soup.search('python logo PNG')
    im = images[0]
    main_color = im.main_color(reduce_size=True)
    assert len(main_color) == 1
    assert main_color[0][0] == 'white'


def test_imageresult_tofile():
    soup = ImageSoup()
    images = soup.search('pyhon site:python.org')
    im = images[0]
    im.to_file()
    STANDARD_NAME = 'image'
    assert os.path.isfile(STANDARD_NAME + '.png') is True
    os.remove(STANDARD_NAME + '.png')

    USER_INPUT_NAME = 'pythonlogo.png'
    im.to_file(USER_INPUT_NAME)
    assert os.path.isfile(USER_INPUT_NAME) is True
    os.remove(USER_INPUT_NAME)


def test_imageresult_verify_valid_file():
    soup = ImageSoup()
    images = soup.search('python site:python.org')
    im = images[0]
    assert im.verify() is True


def test_imageresult_verify_invalid_file():
    URL = 'https://httpstat.us/200'
    im = ImageResult(URL)
    assert im.verify() is False


def test_blacklist():
    bl = Blacklist()
    assert isinstance(bl, Blacklist)
    assert os.path.isfile(bl.filename) is True
    os.remove(bl.filename)


def test_blacklist_add():
    bl = Blacklist()
    bl.add('http://www.python.org')
    assert len(bl.domains) == 1
    assert bl.domains == ['python.org']


def test_blacklist_delete():
    bl = Blacklist()
    bl.delete('python.org')
    assert bl.domains == []


def test_blacklist_reset():
    bl = Blacklist()
    bl.add('http://www.python.org')
    bl.reset()
    assert bl.domains == []


def test_blacklist_query_string():
    bl = Blacklist()
    bl.add('http://www.python.org')
    bl.add('https://github.com/')
    query = '-site:python.org -site:github.com'
    assert bl.query_string() == query
    os.remove(bl.filename)

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#


@pytest.fixture
@pytest.mark.reverse_search
def image_filepath():
    TEST_IMAGE_FILE = 'test_image1.png'
    here = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(here, TEST_IMAGE_FILE)
    assert os.path.isfile(filepath) is True
    return filepath


@pytest.mark.reverse_search
def test_reverse_search_init():
    revsoup = ReverseSearch()
    assert isinstance(revsoup, ReverseSearch)


@pytest.mark.reverse_search
def test_reverse_search_post_search(image_filepath):
    revsoup = ReverseSearch()
    HTML = revsoup.post_image_search_on_google(image_filepath)
    assert isinstance(HTML, str) is True
    assert 'python' in HTML


@pytest.mark.reverse_search
def test_reverse_search_search(image_filepath):
    revsoup = ReverseSearch()
    search_result = revsoup.search(image_filepath)
    assert isinstance(search_result, ReverseSearchResult) is True


@pytest.mark.reverse_search
def test_reverse_search_result_label(image_filepath):
    revsoup = ReverseSearch()
    search_result = revsoup.search(image_filepath)
    expected_label = 'python 3 logo'
    assert search_result.label == expected_label


@pytest.mark.reverse_search
def test_rev_search_result_similar_images(image_filepath):
    revsoup = ReverseSearch()
    search_result = revsoup.search(image_filepath)
    assert isinstance(search_result.similar_images, list)
    assert len(search_result.similar_images) == 100
    assert all(isinstance(i, ImageResult) for i in search_result.similar_images)


