from datetime import datetime

from bson import ObjectId

from .store.comment_model import CommentModel
from .store.comment_repository import CommentRepository


class CommentWriter:
    @staticmethod
    def create_comment(task_id: str, user_id: str, content: str) -> CommentModel:
        comment = CommentModel(
            task_id=task_id,
            user_id=user_id,
            content=content,
        )
        result = CommentRepository.collection().insert_one(comment.to_bson())
        comment.id = result.inserted_id
        return comment

    @staticmethod
    def update_comment(comment: CommentModel, content: str) -> CommentModel:
        comment.content = content
        comment.updated_at = datetime.now()
        CommentRepository.collection().update_one({"_id": comment.id}, {"$set": comment.to_bson()})
        return comment

    @staticmethod
    def delete_comment(comment: CommentModel) -> None:
        CommentRepository.collection().delete_one({"_id": comment.id})
