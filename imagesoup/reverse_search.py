import requests


class ReverseSearch():
    def __init__(self):
filePath = 'D:\\Projetos\\#DEV Python\\ImageSoup\\imagesoup\\agua.png'
searchUrl = 'http://www.google.hr/searchbyimage/upload'
multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
response = requests.post(searchUrl, files=multipart, allow_redirects=False)
fetchUrl = response.headers['Location']

webbrowser.open(fetchUrl)
