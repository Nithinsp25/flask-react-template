import unittest

from apps.backend.modules.comment.internal.store.comment_model import CommentModel


class BaseTestComment(unittest.TestCase):
    def setUp(self):
        self.task_id = "test_task_id"
        self.user_id = "test_user_id"
        self.comment_content = "This is a test comment."
        self.comment = CommentModel(
            task_id=self.task_id,
            user_id=self.user_id,
            content=self.comment_content,
        )
