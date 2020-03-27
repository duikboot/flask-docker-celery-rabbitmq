import logging

from flask_restful import Api, Resource

import config
import tasks

logger = logging.getLogger()

api = Api(prefix=config.API_PREFIX)


class DataProcessingAPI(Resource):
    def post(self):
        logger.info("DataProcessingAPI")
        task = tasks.process_data.delay()

        logger.info("Task: %s", task)

        return {'task_id': task.id}, 200

# data processing endpoint
api.add_resource(DataProcessingAPI, '/process_data')
