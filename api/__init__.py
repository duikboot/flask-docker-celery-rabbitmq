import logging
import time

from flask_restful import Api, Resource
from flask import jsonify

import config
import tasks

LOGGER = logging.getLogger()

api = Api(prefix=config.API_PREFIX)


class TaskStatusAPI(Resource):
    @staticmethod
    def get(task_id):
        task = tasks.celery.AsyncResult(task_id)
        LOGGER.info("TaskStatusAPI")
        LOGGER.info("Task: %s", task)
        if task.state == 'PENDING':
            time.sleep(1)
            response = {
                'queue_state': task.state,
                'status': 'Process is ongoing...',
            }
        elif task.state == 'SUCCESS':

            response = {
                'queue_state': task.state,
                'result': task.wait()
            }
        else:
            response = {
                'queue_state': task.state,
                'result': task.wait()
            }

        return jsonify(response)


class DataProcessingAPI(Resource):
    @staticmethod
    def post():
        LOGGER.info("DataProcessingAPI")
        task = tasks.process_data.delay()

        LOGGER.info("Task: %s", task)

        return {'task_id': task.id}, 200

# data processing endpoint
api.add_resource(DataProcessingAPI, '/process_data')
# task status endpoint
api.add_resource(TaskStatusAPI, '/tasks/<string:task_id>')
