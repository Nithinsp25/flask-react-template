from flask import Blueprint, request, jsonify
from apps.backend.modules.comment.comment_service import CommentService

def register_comment_api(comment_service: CommentService) -> Blueprint:
    comment_api = Blueprint("comment", __name__)

    @comment_api.route("/tasks/<task_id>/comments", methods=["GET"])
    def get_comments(task_id: str):
        comments = comment_service.get_comments_for_task(task_id)
        return jsonify(comments)

    @comment_api.route("/tasks/<task_id>/comments", methods=["POST"])
    def add_comment(task_id: str):
        data = request.get_json()
        # Assuming user_id is available from auth middleware
        user_id = "current_user_id" 
        content = data["content"]
        comment = comment_service.add_comment_to_task(task_id, user_id, content)
        return jsonify(comment), 201

    @comment_api.route("/comments/<comment_id>", methods=["PUT"])
    def update_comment(comment_id: str):
        data = request.get_json()
        # Assuming user_id is available from auth middleware
        user_id = "current_user_id"
        comment = comment_service.update_comment(comment_id, user_id, data)
        return jsonify(comment)

    @comment_api.route("/comments/<comment_id>", methods=["DELETE"])
    def delete_comment(comment_id: str):
        # Assuming user_id is available from auth middleware
        user_id = "current_user_id"
        comment_service.delete_comment(comment_id, user_id)
        return "", 204

    return comment_api
