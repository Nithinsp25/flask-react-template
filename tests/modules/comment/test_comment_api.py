import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

import json
import unittest
from unittest.mock import patch

from flask import Flask

from apps.backend.modules.comment.comment_service import CommentService
from apps.backend.modules.comment.rest_api.comment_api import register_comment_api
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentApi(BaseTestComment):
    def setUp(self):
        super().setUp()
        self.app = Flask(__name__)
        self.comment_service = CommentService()
        self.app.register_blueprint(register_comment_api(self.comment_service))
        self.client = self.app.test_client()

    @patch.object(CommentService, "get_comments_for_task")
    def test_get_comments(self, mock_get_comments):
        mock_get_comments.return_value = [{"content": self.comment_content}]
        response = self.client.get(f"/tasks/{self.task_id}/comments")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["content"], self.comment_content)

    @patch.object(CommentService, "add_comment_to_task")
    def test_add_comment(self, mock_add_comment):
        mock_add_comment.return_value = {"content": self.comment_content}
        response = self.client.post(
            f"/tasks/{self.task_id}/comments",
            data=json.dumps({"content": self.comment_content}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["content"], self.comment_content)

    @patch.object(CommentService, "update_comment")
    def test_update_comment(self, mock_update_comment):
        updated_content = "updated content"
        mock_update_comment.return_value = {"content": updated_content}
        response = self.client.put(
            f"/comments/some_id",
            data=json.dumps({"content": updated_content}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["content"], updated_content)

    @patch.object(CommentService, "delete_comment")
    def test_delete_comment(self, mock_delete_comment):
        response = self.client.delete("/comments/some_id")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
