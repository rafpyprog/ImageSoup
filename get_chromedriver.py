from distutils.version import StrictVersion
import sys
import subprocess
import zipfile

import requests
from bs4 import BeautifulSoup
import lxml

GOOGLE_API = 'https://chromedriver.storage.googleapis.com/'

def get_local_release(chrome_path):
    from subprocess import check_output
    cmd = [chrome_path, '-v']
    release = check_output(cmd).decode()
    number = release.split(' ')[1]
    number = '.'.join(number.split('.')[:2])
    return number


def get_latest_release():
    URL = GOOGLE_API + 'LATEST_RELEASE'
    response = requests.get(URL)
    response.raise_for_status()
    release = response.text.strip()
    return release


def download(version, path=None):
    if path is None:
        path = os.getcwd()
    else:
        path = os.fspath(path)

    is_64bits = sys.maxsize > 2**32
    n_bits = 64 if is_64bits else 32

    # Determines which file to download according to the user platform
    driver_files = {'darwin': 'chromedriver_mac64.zip',
                    'linux': 'chromedriver_linux{}.zip'.format(n_bits),
                    'win32': 'chromedriver_win32.zip'}
    platform_file = driver_files[sys.platform]
    version_file = '/'.join([str(version), platform_file])

    DOWNLOAD_URL = GOOGLE_API + version_file

    print('Downloading file: {}'.format(DOWNLOAD_URL))
    response = requests.get(DOWNLOAD_URL)
    response.raise_for_status()
    path_to_save = os.path.join(path, platform_file)
    with open(path_to_save, 'wb') as f:
        f.write(response.content)
    return os.path.join(path, platform_file)


def unzip(file, path=None):
    if path is None:
        path = os.getcwd()
    else:
        path = os.fspath(path)
    with zipfile.ZipFile(file) as z:
        z.extractall(path)
        return os.path.join(path, z.filelist[0].filename)


def download_chromedriver(version=None, path=None, clean_up=True, set_environ=False):
    '''
        Download a Chromedriver release. If version is None, will download
        the lastest release.
    '''
    if path is None:
        path = os.getcwd()
    else:
        path = os.fspath(path)

    if version is None:
        version = get_latest_release()

    chrome_zip = download(version, path=path)
    executable_path = unzip(chrome_zip, path=path)

    if clean_up is True:
        os.remove(chrome_zip)

    if set_environ is True:
        environ_variable = 'CHROME_DRIVER_PATH'
        os.environ[environ_variable] = executable_path
        print('Chrome path {} on environ variable {}.'
              .format(executable_path, environ_variable))

    return executable_path


def is_updated(chrome_path):
    local = get_local_release(chrome_path)
    latest = get_latest_release()
    print('Local: {} - Latest: {}'.format(local, latest))
    return StrictVersion(local) == StrictVersion(latest)


download_chromedriver(path='D:\\', set_environ=True)


get_local_release(os.environ['CHROME_DRIVER_PATH'])
is_updated(os.environ['CHROME_DRIVER_PATH'])
