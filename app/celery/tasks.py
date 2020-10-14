from celery import Celery

from app.stores.services import create_image_job_process
from app.utils.general import get_config_value

CELERY_BROKER = get_config_value("CELERY_BROKER")
CELERY_BACKEND = get_config_value("CELERY_BACKEND")

app = Celery('task', backend=CELERY_BACKEND, broker=CELERY_BROKER)


@app.task()
def task(image_url, job_id, store_id, image_urls_count):
    create_image_job_process(image_url, job_id, store_id, image_urls_count)
