from typing import Any
from datetime import datetime
from bson import ObjectId

from src.db import posts_collection, users_collection

def create_post(
    user_id: str,
    cocktail_name: str,
    review_score: int=0,
    caption: str = "",
    image_url: str = ""
) -> tuple[dict[str, Any], int]:
    """Create a new post for a user."""
    if not ObjectId.is_valid(user_id):
        return {"error": "Invalid user id."}, 400

    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return {"error": "User not found."}, 404

    if not cocktail_name.strip():
        return {"error": "cocktail_name is required."}, 400

    if not (0 <= review_score <= 5):
        return {"error": "review_score must be between 0 and 5."}, 400

    post = {
        "user_id": user_id,
        "username": user["username"],
        "cocktail_name": cocktail_name.strip(),
        "review_score": review_score,
        "caption": caption.strip(),
        "image_url": image_url.strip(),
        "likes_count": 0,
        "created_at": datetime.now()
    }

    result = posts_collection.insert_one(post)

    post["_id"] = str(result.inserted_id)

    if "created_at" in post:
        post["created_at"] = post["created_at"].isoformat()

    return {"message": "Post created successfully.",
    "post": post
    }, 201

def get_post_by_id(post_id: str) -> tuple[dict[str, Any], int]:
    """Get a single post by id."""
    if not ObjectId.is_valid(post_id):
        return {"error": "Invalid post id."}, 400

    post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if not post:
        return {"error": "Post not found."}, 404

    return post, 200

def delete_post(post_id: str, user_id: str) -> tuple[dict[str, Any], int]:
    """Delete a post (only if it belongs to the given user)."""
    if not ObjectId.is_valid(post_id):
        return {"error": "Invalid post id."}, 400

    if not ObjectId.is_valid(user_id):
        return {"error": "Invalid user id."}, 400

    post = posts_collection.find_one({"_id": ObjectId(post_id)})

    if not post:
        return {"error": "Post not found."}, 404

    if post["user_id"] != user_id:
        return {"error": "You can only delete your own posts."}, 403

    posts_collection.delete_one({"_id": ObjectId(post_id)})

    return {"message": "Post deleted successfully."}, 200

def get_feed_for_user(user_id: str) -> tuple[dict[str, Any], int]:
    """Get a global feed timeline of all user posts with usernames."""
    if not ObjectId.is_valid(user_id):
        return {"error": "Invalid user id."}, 400

    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found."}, 404

    posts = list(posts_collection.aggregate([
        {
            "$addFields": {
                "user_object_id": {"$toObjectId": "$user_id"}
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "user_object_id",
                "foreignField": "_id",
                "as": "author"
            }
        },
        {
            "$unwind": "$author"
        },
        {
            "$sort": {"created_at": -1, "_id": -1}
        },
        {
            "$project": {
                "_id": 1,
                "user_id": 1,
                "cocktail_name": 1,
                "caption": 1,
                "image_url": 1,
                "likes_count": 1,
                "created_at": 1,
                "username": "$author.username"
            }
        }
    ]))

    for post in posts:
        post["_id"] = str(post["_id"])

    return {
        "viewer_id": user_id,
        "viewer_username": user["username"],
        "posts": posts
    }, 200

