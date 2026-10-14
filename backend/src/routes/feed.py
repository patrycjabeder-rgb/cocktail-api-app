from flask import Blueprint, jsonify

from src.services.feed_service import (
    create_post,
    get_post_by_id,
    delete_post,
    get_feed_for_user
)

feed_bp = Blueprint("feed", __name__)

from flask import Blueprint, jsonify, request

@feed_bp.route("/create-post", methods=["POST"])
def add_post():
    """Create a new post."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON data."}), 400

    user_id = data.get("user_id")
    cocktail_name = data.get("cocktail_name")
    caption = data.get("caption", "")
    image_url = data.get("image_url", "")

    if not user_id or not cocktail_name:
        return jsonify({"error": "user_id and cocktail_name are required."}), 400

    result, status = create_post(
        user_id=user_id,
        cocktail_name=cocktail_name,
        caption=caption,
        image_url=image_url
    )
    return jsonify(result), status

@feed_bp.route("/get-post-by-id", methods=["GET"])
def get_post(post_id: str):
    """Get a single post by id."""
    result, status = get_post_by_id(post_id)
    return jsonify(result), status

@feed_bp.route("/delete-a-post", methods=["DELETE"])
def remove_post(post_id: str):
    """Delete a post."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON data."}), 400

    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required."}), 400

    result, status = delete_post(post_id, user_id)
    return jsonify(result), status

from flask import request

@feed_bp.route("/feed", methods=["GET"])
def get_feed():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    result, status = get_feed_for_user(user_id)
    return jsonify(result), status