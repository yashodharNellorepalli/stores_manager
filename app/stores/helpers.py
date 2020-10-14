import datetime
import urllib
from functools import reduce

from PIL import Image
from bson.objectid import ObjectId


def get_perimeter(image):
    if not image:
        return 0

    return 2*(image.get('height') + image.get('width'))


def get_perimeter_of_all_images(image_urls, all_images_info):
    return reduce(lambda x, y: get_perimeter(all_images_info.get(x, None)) + get_perimeter(all_images_info.get(y, None)), image_urls)


def get_size_of_image(image_url):
    try:
        image = Image.open(urllib.request.urlopen(image_url))
        width, height = image.size
        return height, width
    except Exception as e:
        return None, None


def get_image_urls_count(visits):
    image_urls_count = 0

    for visit in visits:
        image_urls_count += len(visit.get('image_url'))

    return image_urls_count


def convert_time_format(e, source_format, destination_format):
    return datetime.datetime.strptime(e, source_format).strftime(destination_format)


def get_object_id(_id):
    try:
        x = ObjectId(_id)
        return x
    except Exception as e:
        return None
