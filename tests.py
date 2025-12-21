import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api

from api import (
    DataProcessingAPI,
    GroupDataProcessingAPI,
    TaskStatusAPI,
)


class TestAPIs(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(DataProcessingAPI, "/process_data")
        self.api.add_resource(GroupDataProcessingAPI, "/bulk_process_data")
        self.api.add_resource(TaskStatusAPI, "/tasks/<string:task_id>")
        self.client = self.app.test_client()

    @patch("api.tasks.process_data")
    def test_data_processing_api_post(self, mock_process_data):
        mock_task = MagicMock()
        mock_task.id = "test_task_id"
        mock_process_data.delay.return_value = mock_task

        response = self.client.post("/process_data")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"task_id": "test_task_id"})

    @patch("api.tasks.process_multiple")
    def test_group_data_processing_api_get(self, mock_process_multiple):
        mock_task = "test_group_task_id"
        mock_process_multiple.return_value = mock_task

        response = self.client.get("/bulk_process_data")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"task_id": "test_group_task_id"})

    @patch("api.tasks.celery.AsyncResult")
    def test_task_status_api_get_pending(self, mock_async_result):
        mock_task = MagicMock()
        mock_task.state = "PENDING"
        mock_async_result.return_value = mock_task

        response = self.client.get("/tasks/test_task_id")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {"queue_state": "PENDING",
                            "status": "Process is ongoing..."}
        )

    @patch("api.tasks.celery.AsyncResult")
    def test_task_status_api_get_success(self, mock_async_result):
        mock_task = MagicMock()
        mock_task.state = "SUCCESS"
        mock_task.get.return_value = {"key": "value"}
        mock_async_result.return_value = mock_task

        response = self.client.get("/tasks/test_task_id")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {"queue_state": "SUCCESS",
                            "result": {"key": "value"}}
        )

    @patch("api.tasks.celery.AsyncResult")
    def test_task_status_api_get_other_state(self, mock_async_result):
        mock_task = MagicMock()
        mock_task.state = "FAILURE"
        mock_task.get.return_value = {"error": "some error"}
        mock_async_result.return_value = mock_task

        response = self.client.get("/tasks/test_task_id")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {"queue_state": "FAILURE",
                            "result": {"error": "some error"}}
        )


if __name__ == "__main__":
    unittest.main()
