from typing import Optional

from bson import ObjectId

from .store.comment_model import CommentModel
from .store.comment_repository import CommentRepository


class CommentReader:
    @staticmethod
    def get_comments_by_task_id(task_id: str) -> list[CommentModel]:
        comments_bson = CommentRepository.collection().find({"task_id": task_id})
        return [CommentModel.from_bson(comment) for comment in comments_bson]

    @staticmethod
    def get_comment_by_id(comment_id: str) -> Optional[CommentModel]:
        comment_bson = CommentRepository.collection().find_one({"_id": ObjectId(comment_id)})
        if not comment_bson:
            return None
        return CommentModel.from_bson(comment_bson)
