import sys

import requests
from bs4 import BeautifulSoup
import lxml

def get_latest_release():
    URL = 'https://sites.google.com/a/chromium.org/chromedriver/downloads'
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'lxml')
    RELEASES = {'id': 'sites-canvas-main-content'}
    latest = soup.find('div', attrs=RELEASES).findAll('a')[1]
    latest_version_number = latest.text.split(' ')[-1]
    print('Latest release: {}'.format(latest_version_number))
    return latest_version_number

version = get_latest_release()


def download(version, mode=64):
    '''
        mode(int): 64 or 32 bits
    '''
    if sys.platform == 'darwin':
        filename = 'chromedriver_mac64.zip'
    elif sys.platform == 'Windows':
        filename = 'chromedriver_win32.zip'
    else:
        filename = 'chromedriver_linux{}.zip'.format(mode)

    fil


    BASE_URL = 'https://chromedriver.storage.googleapis.com/'
    URL = BASE_URL + '?delimiter=/&prefix={}/'
    response = requests.get(URL.format(version))
    soup = BeautifulSoup(response.text, 'lxml')
    if system = 'win':
    files = [i.text for i in soup.findAll('key')]




latest_files_URL = latest['href']
headers = {'User-Agent': user_agent}
response = requests.get(latest_files_URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
soup
files = soup.findAll('a')


r = requests.get(URL)

data = [i.find('key') for i in soup.findAll('contents')]

for i in data:
    print(i.text)
