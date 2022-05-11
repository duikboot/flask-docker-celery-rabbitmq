import logging
import random
import time

from celery import Celery, group, signature

import config

LOGGER = logging.getLogger()


def make_celery():
    celery = Celery(__name__, broker=config.CELERY_BROKER)
    celery.conf.update(config.as_dict())
    return celery


celery = make_celery()


@celery.task
def error_handler(request, exc, traceback):
    LOGGER.error('Task {0} raised exception: {1!r}\n{2!r}'.format(
        request.id, exc, traceback))


@celery.task
def process_data():
    LOGGER.info("Process data")
    sleep = 30*random.random()
    if sleep > 25:
        raise ValueError("TEST")

    time.sleep(sleep)
    return {"succes": "ok", "sleep": round(sleep, 2)}


@celery.task(bind=True)
def process_multiple(self,):
    LOGGER.info("Process bulk data: %s", self)
    # batches = [signature("process_data") for i in range(30)]
    # jobs = process_data.chunks(list(range(10)), 7).group()
    jobs = group([
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
    ], link_error=error_handler.s(),
    )
    result = jobs.apply_async()
    LOGGER.info("jobs, %r", jobs)

    return {"succes": "ok", "results": result}
