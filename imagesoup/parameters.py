FILE_TYPE_OPTIONS = {}

USAGE_RIGHT_OPTIONS = {}

ASPECT_RATIO_OPTIONS = {'tall': 't', 'square': 's', 'wide': 'w',
                        'panoramic': 'xw'}

IMAGE_SIZE_OPTIONS = {'any': '', 'icon': 'i', 'medium': 'm', 'large': 'l',
                      'exactly': 'ex', '400x300+': 'qsvga', '640x480+': 'vga',
                      '800x600+': 'svga', '1024x768+': 'xga', '2mp+': '2mp',
                      '4mp+': '4mp', '6mp+': '6mp', '8mp+': '8mp',
                      '10mp+': '10mp', '12mp+': '12mp', '15mp+': '15mp',
                      '20mp+': '20mp', '40mp+': '40mp', '70mp+': '70mp'}


def aspect_ratio_paramenter(option):
    if not option:
        return None

    ASPECT_RATIO_PARAM = 'iar'
    return ASPECT_RATIO_PARAM + ':' + ASPECT_RATIO_OPTIONS[option]


def image_size_parameter(option):
    if not option:
        return None

    IMAGE_SIZE_PARAM = 'isz'
    if isinstance(option, (tuple, list)):
        width, height = option
        return IMAGE_SIZE_PARAM + ':{},iszw:{},iszh:{}'.format(IMAGE_SIZE_OPTIONS['exactly'], width, height)
    else:
        return IMAGE_SIZE_PARAM + ':' + IMAGE_SIZE_OPTIONS[option]


def image_aspect_parameters(aspect_ratio, image_size):
    if any([aspect_ratio, image_size]) is False:
        return None
    else:
        IMAGE_RELATED = 'tbs='
        options = ','.join([i for i in [aspect_ratio, image_size] if i is not None])
        return '{}{}'.format(IMAGE_RELATED, options)


def query_builder(query, image_size=None, aspect_ratio=None, page_number=0):
    if query is None:
        raise ValueError('query must have a value.')

    SEARCH_TYPE = 'tbm'
    IMAGES = 'isch'
    SEARCH_TYPE_PARAM = '='.join([SEARCH_TYPE, IMAGES])
    BASE_URL = 'https://www.google.com/search?' + SEARCH_TYPE_PARAM

    # Add page number
    PAGE_NUMBER = 'ijn'
    page_number_param = '='.join([PAGE_NUMBER, str(page_number)])
    URL = '&'.join([BASE_URL, page_number_param])

    # Add query value
    QUERY_TYPE = 'q'
    query_param = '='.join([QUERY_TYPE, str(query)])
    URL = '&'.join([URL, query_param])

    # Add image aspects parameters
    iar = aspect_ratio_paramenter(aspect_ratio)
    isz = image_size_parameter(image_size)
    image_aspect_param = image_aspect_parameters(iar, isz)
    if image_aspect_param is not None:
        URL = '&'.join([URL, image_aspect_param])

    return URL
