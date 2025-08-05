import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

import unittest
from unittest.mock import patch, MagicMock

from apps.backend.modules.comment.comment_service import CommentService
from apps.backend.modules.comment.errors import CommentNotFound, CommentForbidden
from apps.backend.modules.comment.internal.store.comment_model import CommentModel
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentService(BaseTestComment):
    @patch("apps.backend.modules.comment.comment_service.CommentReader")
    def test_get_comments_for_task(self, mock_comment_reader):
        mock_comment_reader.get_comments_by_task_id.return_value = [self.comment]
        service = CommentService()
        comments = service.get_comments_for_task(self.task_id)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]["content"], self.comment_content)

    @patch("apps.backend.modules.comment.comment_service.CommentWriter")
    def test_add_comment_to_task(self, mock_comment_writer):
        mock_comment_writer.create_comment.return_value = self.comment
        service = CommentService()
        comment = service.add_comment_to_task(self.task_id, self.user_id, self.comment_content)
        self.assertEqual(comment["content"], self.comment_content)

    @patch("apps.backend.modules.comment.comment_service.CommentReader")
    @patch("apps.backend.modules.comment.comment_service.CommentWriter")
    def test_update_comment(self, mock_comment_writer, mock_comment_reader):
        mock_comment_reader.get_comment_by_id.return_value = self.comment
        mock_comment_writer.update_comment.return_value = self.comment
        service = CommentService()
        updated_content = "This is an updated comment."
        comment = service.update_comment(str(self.comment.id), self.user_id, {"content": updated_content})
        self.assertEqual(comment["content"], self.comment_content)

    @patch("apps.backend.modules.comment.comment_service.CommentReader")
    def test_update_comment_not_found(self, mock_comment_reader):
        mock_comment_reader.get_comment_by_id.return_value = None
        service = CommentService()
        with self.assertRaises(CommentNotFound):
            service.update_comment("some_id", self.user_id, {"content": "update"})

    @patch("apps.backend.modules.comment.comment_service.CommentReader")
    def test_update_comment_forbidden(self, mock_comment_reader):
        mock_comment_reader.get_comment_by_id.return_value = self.comment
        service = CommentService()
        with self.assertRaises(CommentForbidden):
            service.update_comment(str(self.comment.id), "another_user", {"content": "update"})

    @patch("apps.backend.modules.comment.comment_service.CommentReader")
    @patch("apps.backend.modules.comment.comment_service.CommentWriter")
    def test_delete_comment(self, mock_comment_writer, mock_comment_reader):
        mock_comment_reader.get_comment_by_id.return_value = self.comment
        service = CommentService()
        service.delete_comment(str(self.comment.id), self.user_id)
        mock_comment_writer.delete_comment.assert_called_once_with(self.comment)


if __name__ == "__main__":
    unittest.main()
