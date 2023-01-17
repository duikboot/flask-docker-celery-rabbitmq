import logging

from flask import jsonify
from flask_restful import Api, Resource

import config
import tasks

LOGGER = logging.getLogger()

api = Api(prefix=config.API_PREFIX)


def task(task_id):
    task = tasks.celery.AsyncResult(task_id)
    LOGGER.info("TaskStatusAPI")
    state = task.state
    LOGGER.info("Task: state: %r", state)
    if state == 'PENDING':
        response = {
            'queue_state': state,
            'status': 'Process is ongoing...',
        }
    elif state == 'SUCCESS':

        response = {
            'queue_state': state,
            'result': task.wait()
        }
    else:
        response = {
            'queue_state': state,
            'result': task.wait()
        }
    return response


class TaskStatusAPI(Resource):
    @staticmethod
    def get(task_id):
        response = task(task_id)
        return jsonify(response)


class DataProcessingAPI(Resource):
    @staticmethod
    def post():
        LOGGER.info("DataProcessingAPI")
        task = tasks.process_data.delay()

        LOGGER.info("Task: %s", task)

        return {'task_id': task.id}, 200


class GroupDataProcessingAPI(Resource):
    @staticmethod
    def get():
        LOGGER.info("DataProcessingAPI")
        task = tasks.process_multiple()

        LOGGER.info("Task: %s", task)

        return {'task_id': "{}".format(task)}, 200


# data processing endpoint
api.add_resource(DataProcessingAPI, '/process_data')
api.add_resource(GroupDataProcessingAPI, '/bulk_process_data')
# task status endpoint
api.add_resource(TaskStatusAPI, '/tasks/<string:task_id>')
