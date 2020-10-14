from flask import Blueprint, jsonify, request

from app.celery.tasks import task
from app.utils.constants import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .helpers import get_image_urls_count
from .services import get_job_info, insert_store_visits, get_stores_info, get_stores_visit_info

stores_module = Blueprint('stores', __name__, url_prefix='/stores')


@stores_module.route('/api/status', methods=['GET'])
def get_job():
    request_data = request.args
    job_id = request_data.get('job_id')
    job_info = get_job_info(job_id)

    if job_info is None:

        response_data = {

        }

        return jsonify(response_data), HTTP_400_BAD_REQUEST

    if job_info.get('status') == 'failed':
        response_data = {
            'status': 'failed',
            'job_id': job_id,
            'error': job_info.get('error', [])
        }

        return jsonify(response_data), HTTP_200_OK

    response_data = {
        'status': job_info.get('status'),
        'job_id': job_id
    }

    return jsonify(response_data), HTTP_200_OK


@stores_module.route('/api/submit', methods=['POST'])
def submit_job():
    request_data = request.get_json()
    count_ = request_data.get('count')
    visits = request_data.get('visits')

    if count_ != len(visits):
        response_data = {
            'error': 'count is not equal to visits length'
        }

        return jsonify(response_data), HTTP_400_BAD_REQUEST

    image_urls_count = get_image_urls_count(visits)
    store_visits_input = {
        'count': count_,
        'visits': visits,
        'status': 'ongoing',
        'error': [],
        'image_urls_count': image_urls_count,
        'success_count': 0
    }

    store_visits = insert_store_visits(store_visits_input)
    job_id = str(store_visits)

    for visit in visits:
        image_urls = visit.get('image_url')
        store_id = visit.get('store_id')

        for image_url in image_urls:
            task.delay(image_url, job_id, store_id, image_urls_count)

    response_data = {
        'job_id': job_id
    }

    return jsonify(response_data), HTTP_201_CREATED


@stores_module.route('/api/visits', methods=['GET'])
def get_visits():
    request_data = request.args
    area_code = request_data.get('area', None)
    store_id = request_data.get('store', None)
    start_date = request_data.get('startdate', None)
    end_date = request_data.get('enddate', None)

    stores_info = get_stores_info(store_id, area_code)
    store_ids = list(stores_info.keys())

    if len(store_ids) == 0:
        response_data = {
            "error": "Store_id doesnt exist"
        }

        return jsonify(response_data), HTTP_400_BAD_REQUEST

    stores_visits_info = get_stores_visit_info(store_ids, start_date, end_date)

    results = []

    for store_id, visits_info in stores_visits_info.items():
        store = stores_info.get(store_id, None)

        if not store:
            continue

        results.append({
            'store_id': store_id,
            'area': store.get('area_code'),
            'store_name': store.get('store_name'),
            'data': list({'date': visit_date, 'perimeter': perimeter} for visit_date, perimeter in visits_info.items())
        })

    response_data = {
        "results": results
    }

    return jsonify(response_data), HTTP_200_OK
