from collections import Counter

import webcolors


CSS3_COLORS = webcolors.CSS3_NAMES_TO_HEX.keys()

def color_analysis(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # initialize a Counter starting from zero
    CSS3_COLORS = webcolors.css3_names_to_hex.keys()
    color_counter = Counter({color:0 for color in Counter(CSS3_COLORS)})
    for pixel_count, RGB in image.getcolors(image.width * image.height):
        color_name = get_colour_name(RGB)
        color_counter[color_name] += pixel_count

    # Calculate percent for each color
    for color in color_counter:
        color_counter[color] = color_counter[color] / (image.width * image.height)

    return color_counter


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        colour_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        colour_name = closest_colour(requested_colour)
    return colour_name
