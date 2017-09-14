from distutils.version import StrictVersion
import os
import platform
import re
import sys
import subprocess
from subprocess import Popen, PIPE
import zipfile

import fire
import requests
from bs4 import BeautifulSoup
import lxml
from selenium.common.exceptions import WebDriverException

GOOGLE_API = 'https://chromedriver.storage.googleapis.com/'


def parse_chromedriver_version(cmd_stdout):
    '''
        cmd_stdout (string): Output from chromedriver -v
    '''
    CHROMEDRIVER_VERSION_PATTERN = '\d+\.\d+'
    version = re.search(CHROMEDRIVER_VERSION_PATTERN, cmd_stdout)
    if version:
        return version.group()
    else:
        raise Exception('Unable to parse Chromedriver version {}'
                        .format(cmd_stdout))


def get_local_release(executable_path='chromedriver'):
    cmd = [executable_path, '-v']
    try:
        process = Popen(cmd, env=os.environ,
                        close_fds=platform.system() != 'Windows',
                        stdout=PIPE, stderr=PIPE)
    except OSError:
        msg = '{} executable needs to be in PATH.'
        raise WebDriverException(
            msg.format(os.path.basename(executable_path)))
    else:
        stdout = process.communicate()[0]
        version = parse_chromedriver_version(stdout.decode())
    return version


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


def get_chrome(version=None, path=None, clean_up=True, set_environ=False):
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

    if sys.platform == 'linux':
        os.system('chmod +x ' + executable_path)

    if clean_up is True:
        os.remove(chrome_zip)

    if set_environ is True:
        environ_variable = 'CHROME_DRIVER_PATH'
        os.environ[environ_variable] = executable_path
        print('Chrome path {} on environ variable {}.'
              .format(executable_path, environ_variable))

    return executable_path


def is_updated(executable_path='chromedriver'):
    local = get_local_release(executable_path)
    latest = get_latest_release()
    return StrictVersion(local) == StrictVersion(latest)


def update():
    if is_updated():
        installed_release = get_local_release()
        print('The installed release({}) is already up to date.'
        .format(installed_release))
    else:
        return None

if __name__ == '__main__':
    fire.Fire({'update': update})
