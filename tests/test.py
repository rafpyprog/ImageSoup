import pytest

from imagesoup import ImageSoup


def test_creating_soup():
    soup = ImageSoup()
    assert isinstance(soup, ImageSoup)
