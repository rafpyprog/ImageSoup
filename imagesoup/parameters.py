from six.moves.urllib.parse import urlencode


class AspectRatio():
    def __init__(self):
        self.name = 'iar'
        self.values = {'tall': 't',
                       'square': 's',
                       'wide': 'w',
                       'panoramic': 'xw'}

    def get_param(self, value):
        return self.name + ':' + self.values[value]


class ImageSize():
    def __init__(self):
        self.name = 'isz'
        self.values = {'any': '',
                       'icon': 'i',
                       'medium': 'm',
                       'large': 'l',
                       'exactly': 'ex'}

    def get_param(self, value):
        if isinstance(value, (tuple, list)):
            width, height = value
            return self.name + ':{},iszw:{},iszh:{}'.format(self.values['exactly'], width, height)
        else:            
            return self.name + ':' + self.values[value]

i = ImageSize()
i.get_param([200, 200])


class IMAGE_ASPECTS():
        '''
    Set of suported image size parameters.
    '''
    ANY = ''
    ICON = 'i'
    MEDIUM = 'm'
    LARGE = 'l'

    LARGER_THAN_400_300 = 'qsvga'
    LARGER_THAN_640_480 = 'vga'
    LARGER_THAN_800_600 = 'svga'
    LARGER_THAN_1024_768 = 'xga'

    EXACTLY = 'ex'

    LARGER_THAN_2MP = '2mp'
    LARGER_THAN_4MP = '4mp'
    LARGER_THAN_6MP = '6mp'
    LARGER_THAN_8MP = '8mp'
    LARGER_THAN_10MP = '10mp'
    LARGER_THAN_12MP = '12mp'
    LARGER_THAN_15MP = '15mp'
    LARGER_THAN_20MP = '20mp'
    LARGER_THAN_40MP = '40mp'
    LARGER_THAN_70MP = '70mp'

class URLParameters():
    ALL_THESE_WORDS = 'as_q'
    IMAGE_ASPECTS = 'tbs'
    PAGE_NUMBER = 'ijn'
    QUERY = 'q'
    SEARCH_TYPE = 'tbm'


def query_builder(query, image_size=None, page_number=None):
    IMAGE_SEARCH = 'isch'

    param = URLParameters()

    params = {param.ALL_THESE_WORDS: query,
              param.SEARCH_TYPE: IMAGE_SEARCH,
              param.IMAGE_SIZE: image_size,
              param.PAGE_NUMBER: str(page_number)}

    base_url = 'https://www.google.com/search?'
    url = base_url + '&'.join([param + '=' + value for param, value in params.items() if value])
    return url


https://www.google.com/search?as_st=y&tbm=isch&as_q=folheto+supermercado&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=isz:l,iar:t

query_builder('python', page_number=1, image_size=Size.ICON)
