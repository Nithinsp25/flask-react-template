from typing import TypedDict, Optional

class Comment(TypedDict):
    id: str
    task_id: str
    user_id: str
    content: str
    created_at: str
    updated_at: str

class CommentUpdate(TypedDict, total=False):
    content: Optional[str]
