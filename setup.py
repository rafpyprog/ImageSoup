import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "imagesoup",
    version = "0.0.5",
    author = "Rafael Alves Ribeiro",
    author_email = "rafael.alves.ribeiro@gmail.com",
    description = ("A Python library designed for quick search and "
                    "downloading images from Google Images."),
    license = "MIT",
    keywords = "search image google",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['imagesoup', 'tests'],
    install_requires=['bs4',
                      'pillow',
                      'requests',
                      'webcolors',
                     ],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
    ],
)
