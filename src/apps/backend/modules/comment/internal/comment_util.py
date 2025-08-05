from .store.comment_model import CommentModel
from ..types import Comment


class CommentUtil:
    @staticmethod
    def to_dict(comment: CommentModel) -> Comment:
        return {
            "id": str(comment.id),
            "task_id": comment.task_id,
            "user_id": comment.user_id,
            "content": comment.content,
            "created_at": str(comment.created_at),
            "updated_at": str(comment.updated_at),
        }
