import random
import time

from app.utils.db_connections import get_stores_master_collection
from .helpers import get_perimeter_of_all_images, get_size_of_image, convert_time_format, get_object_id
from ..utils.constants import DATE_FORMAT, DATE_TIME_FORMAT

stores_master_collection = get_stores_master_collection()


def get_job_info(job_id):
    _id = get_object_id(job_id)

    filter_params = {
        '_id': _id
    }
    job_info = stores_master_collection.store_visits.find_one(filter_params, {"_id": 0})

    return job_info


def insert_store_visits(store_visits):
    x = stores_master_collection.store_visits.insert_one(store_visits)
    return x.inserted_id


def get_stores_info(store_id, area_code):
    filter_params = {}

    if area_code:
        filter_params['area_code'] = area_code

    if store_id:
        filter_params['store_id'] = store_id

    stores_info = {store.get('store_id'): store for store in list(stores_master_collection.stores.find(filter_params, {'_id': 0}))}

    return stores_info


def get_stores_visit_info(store_ids, start_date, end_date):
    filter_params = dict()
    filter_params['visits.visit_time'] = {}

    if start_date:
        filter_params['visits.visit_time']['$gte'] = start_date

    if end_date:
        filter_params['visits.visit_time']['$lte'] = end_date

    if not filter_params['visits.visit_time']:
        del filter_params['visits.visit_time']

    if store_ids:
        filter_params['visits.store_id'] = {
            '$in': store_ids
        }

    all_store_visits = list(stores_master_collection.store_visits.find(filter_params, {'_id': 0}))
    stores_visits_info = {}
    all_image_urls = []

    for store_visits in all_store_visits:
        for store_visit in store_visits.get('visits'):
            store_id = store_visit.get('store_id')
            visit_date = convert_time_format(store_visit.get('visit_time'), DATE_TIME_FORMAT, DATE_FORMAT)
            image_urls = store_visit.get('image_url')

            if stores_visits_info.get(store_id, None) is None:
                stores_visits_info[store_id] = {}

            if stores_visits_info[store_id].get(visit_date, None) is None:
                stores_visits_info[store_id][visit_date] = []

            stores_visits_info[store_id][visit_date].extend(image_urls)
            all_image_urls.extend(image_urls)

    all_images_info = get_all_images_info(all_image_urls)

    for store_id, visits_info in stores_visits_info.items():
        for visit_date, image_urls in visits_info.items():
            stores_visits_info[store_id][visit_date] = get_perimeter_of_all_images(image_urls, all_images_info)

    return stores_visits_info


def get_all_images_info(image_urls):
    filter_params = dict()

    if image_urls:
        filter_params['image_url'] = {
            '$in': image_urls
        }

    return {image_info.get('image_url'): image_info for image_info in list(stores_master_collection.images.find(filter_params, {'_id': 0}))}


def create_image_job_process(image_url, job_id, store_id, image_urls_count):
    # fetch height, width of image_url
    height, width = get_size_of_image(image_url)

    if height is None or width is None:
        # update job status invalid image
        update_job_invalid(job_id, image_url, error_message="image download fail")
        return

    stores_info = get_stores_info(store_id, None)

    if len(stores_info.keys()) == 0:
        update_job_invalid(job_id, image_url, error_message=f"StoreId : {store_id} doesnt exist")
        return

    # sleep for 0.1 to 0.4 secs
    random_number = random.randint(1, 4)
    time.sleep(random_number / 10)
    # insert image_url,height, width
    insert_image(image_url, height, width)
    update_job_success(job_id, image_urls_count)


def update_job_success(job_id, image_urls_count):
    _id = get_object_id(job_id)

    filter_params = {
        '_id': _id
    }

    set_value = {
        '$inc': {
            'success_count': 1
        }
    }

    stores_master_collection.store_visits.update_one(filter_params, set_value)
    update_completed_status(job_id, image_urls_count)


def update_completed_status(job_id, image_urls_count):
    _id = get_object_id(job_id)

    filter_params = {
        '_id': _id,
        'success_count': image_urls_count
    }

    set_value = {
        '$set': {
            'status': 'completed'
        }
    }

    stores_master_collection.store_visits.update_one(filter_params, set_value)


def update_job_invalid(job_id, image_url, error_message):
    _id = get_object_id(job_id)
    filter_params = {
        '_id': _id
    }

    set_query = {
        '$push': {
            'error': {
                'image_url': image_url,
                'error': error_message
            }
        },
        '$set': {
            'status': 'failed'
        }
    }

    stores_master_collection.store_visits.update_one(filter_params, set_query)


def insert_image(image_url, height, width):
    input_params = {
        'image_url': image_url,
        'height': height,
        'width': width
    }

    stores_master_collection.images.insert_one(input_params)
