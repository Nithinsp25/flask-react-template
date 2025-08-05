from werkzeug.exceptions import NotFound, Forbidden

class CommentNotFound(NotFound):
    def __init__(self, comment_id: str):
        super().__init__(f"Comment with id {comment_id} not found")

class CommentForbidden(Forbidden):
    def __init__(self):
        super().__init__("You don't have permission to perform this action on this comment")
