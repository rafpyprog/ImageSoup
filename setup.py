import os
from setuptools import setup

from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

about = {}
with open(os.path.join(here, 'imagesoup', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

packages = ['imagesoup']

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    license=about['__license__'],
    keywords = "search image google",
    url = about['__url__'],
    packages=packages,
    install_requires=['beautifulsoup4>=4.5',
                      'pillow',
                      'requests',
                      'webcolors',
                     ],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
    ],
)
