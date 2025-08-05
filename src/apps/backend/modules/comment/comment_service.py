from apps.backend.modules.comment.internal.comment_reader import CommentReader
from apps.backend.modules.comment.internal.comment_writer import CommentWriter
from apps.backend.modules.comment.internal.comment_util import CommentUtil
from apps.backend.modules.comment.types import Comment, CommentUpdate
from apps.backend.modules.comment.errors import CommentNotFound, CommentForbidden

class CommentService:
    def get_comments_for_task(self, task_id: str) -> list[Comment]:
        comments = CommentReader.get_comments_by_task_id(task_id)
        return [CommentUtil.to_dict(comment) for comment in comments]

    def add_comment_to_task(self, task_id: str, user_id: str, content: str) -> Comment:
        comment = CommentWriter.create_comment(task_id, user_id, content)
        return CommentUtil.to_dict(comment)

    def update_comment(self, comment_id: str, user_id: str, updates: CommentUpdate) -> Comment:
        comment = CommentReader.get_comment_by_id(comment_id)
        if not comment:
            raise CommentNotFound(comment_id)
        if comment.user_id != user_id:
            raise CommentForbidden()
        
        updated_comment = CommentWriter.update_comment(comment, updates["content"])
        return CommentUtil.to_dict(updated_comment)

    def delete_comment(self, comment_id: str, user_id: str) -> None:
        comment = CommentReader.get_comment_by_id(comment_id)
        if not comment:
            raise CommentNotFound(comment_id)
        if comment.user_id != user_id:
            raise CommentForbidden()
        CommentWriter.delete_comment(comment)
