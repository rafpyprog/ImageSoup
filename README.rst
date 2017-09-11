ImageSoup: Image Searching for Humans
=====================================


.. image:: https://img.shields.io/pypi/v/imagesoup.svg
  :target: https://pypi.python.org/pypi/imagesoup

.. image:: https://img.shields.io/pypi/l/imagesoup.svg
  :target: https://pypi.python.org/pypi/imagesoup

.. image:: https://travis-ci.org/rafpyprog/ImageSoup.svg?branch=master
  :target: https://travis-ci.org/rafpyprog/ImageSoup

.. image:: https://codecov.io/gh/rafpyprog/ImageSoup/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/rafpyprog/ImageSoup

  
Quick Tutorial  
--------------

.. code-block:: python
    
    >>> from imagesoup import ImageSoup
    >>>
    >>> soup = ImageSoup()    
    >>> images = soup.search('"Arya Stark"', n_images=10)
    >>>
    >>> arya = images[0]
    >>> arya.URL
    'https://upload.wikimedia.org/wikipedia/en/3/39/Arya_Stark-Maisie_Williams.jpg'
    >>> arya.show()
.. image:: https://upload.wikimedia.org/wikipedia/en/3/39/Arya_Stark-Maisie_Williams.jpg

.. code-block:: python

    >>> arya.size
    (300, 404)
    >>> arya.dpi
    (72, 72)
    >>> arya.color_count
    7269
    >>> arya.main_color(n=2)
    [('black', 0.6219224422442244), ('darkslategrey', 0.27796204620462045)]
    >>> arya.to_file('arya.jpg')

Installation
------------

To install ImageSoup, simply use pip:

.. code-block:: bash

    $ pip install imagesoup

Advanced Search
---------------

**image_size:** string, tuple(width, height)
    Find images in any size you need.

* (width, height)


* icon
* medium
* large


* 400x300+
* 640x480+
* 800x600+
* 1024x768+


* 2mp+
* 4mp+
* 8mp+
* 10mp+
* 12mp+
* 15mp+
* 20mp+
* 40mp+
* 70mp+


**aspect_ratio:** string
    Specify the shape of images.

* tall
* square
* wide
* panoramic

.. code-block:: python

    >>> from imagesoup import ImageSoup
    >>>
    >>> soup = ImageSoup()
    >>> images = soup.search('Cersei Lannister', image_size='icon', aspect_ratio='square')
    >>>
    >>> im = images[0]
    >>> im.URL
    'http://cdn.images.express.co.uk/img/dynamic/galleries/64x64/264415.jpg'
    >>> im.size
    (64, 64)
    >>> im.show()
.. image:: http://cdn.images.express.co.uk/img/dynamic/galleries/64x64/264415.jpg

    


