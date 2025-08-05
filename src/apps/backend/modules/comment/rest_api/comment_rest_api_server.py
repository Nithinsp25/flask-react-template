from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from ..comment_service import CommentService
from .comment_api import register_comment_api


class CommentRestApiServer:
    @staticmethod
    def create(db: SQLAlchemy) -> Blueprint:
        comment_service = CommentService(db=db)
        return register_comment_api(comment_service)
