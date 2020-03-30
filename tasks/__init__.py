import logging
import time

from celery import Celery
import config

LOGGER = logging.getLogger()


def make_celery():
    celery = Celery(__name__, broker=config.CELERY_BROKER)
    celery.conf.update(config.as_dict())
    return celery


celery = make_celery()


@celery.task(bind=True)
def process_data(self):
    LOGGER.info("Process data: %s", self)
    time.sleep(30)
    return {"succes": "ok"}
