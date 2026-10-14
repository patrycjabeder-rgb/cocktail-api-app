import pytest

from src.db import users_collection
from src.services.feed_service import (
    create_post,
    get_post_by_id,
    delete_post,
    get_feed_for_user
)
from src.services.user_accounts_service import create_user, delete_user


def get_user_id(username: str) -> str:
    user = users_collection.find_one({"username": username})
    return str(user["_id"])


def extract_post_identifier(post_obj: dict):
    return post_obj.get("id") or post_obj.get("_id") or post_obj.get("post_id")


def cleanup_user(username: str, password: str = "ValidPassword1!"):
    user = users_collection.find_one({"username": username})
    if user:
        delete_user(username, password)


def test_create_post_success():
    cleanup_user("feed_test_user")
    create_user("feed_test_user", "feed_test_user@example.com", "ValidPassword1!")

    user_id = get_user_id("feed_test_user")

    result, status = create_post(
        user_id,
        "Mojito",
        5,
        "This is a test post",
        "https://example.com/mojito.jpg",
    )

    assert status == 201
    assert result["message"] == "Post created successfully."
    assert "post" in result
    assert isinstance(result["post"], dict)
    assert result["post"]["cocktail_name"] == "Mojito"
    assert result["post"]["caption"] == "This is a test post"

    post_id = extract_post_identifier(result["post"])
    assert post_id is not None

    delete_post(str(post_id), user_id)
    delete_user("feed_test_user", "ValidPassword1!")


def test_get_post_by_id_success():
    cleanup_user("feed_test_user")
    create_user("feed_test_user", "feed_test_user@example.com", "ValidPassword1!")
    user_id = get_user_id("feed_test_user")

    create_result, create_status = create_post(
        user_id,
        "Negroni",
        5,
        "Post for get by id test",
        "https://example.com/negroni.jpg",
    )
    assert create_status == 201

    post_id = extract_post_identifier(create_result["post"])
    assert post_id is not None

    result, status = get_post_by_id(str(post_id))

    assert status == 200
    assert isinstance(result, dict)

    delete_post(str(post_id), user_id)
    delete_user("feed_test_user", "ValidPassword1!")


def test_delete_post_success():
    cleanup_user("feed_test_user")
    create_user("feed_test_user", "feed_test_user@example.com", "ValidPassword1!")
    user_id = get_user_id("feed_test_user")

    create_result, create_status = create_post(
        user_id,
        "Martini",
        5,
        "Post to delete",
        "https://example.com/martini.jpg",
    )
    assert create_status == 201

    post_id = extract_post_identifier(create_result["post"])
    assert post_id is not None

    result, status = delete_post(str(post_id), user_id)

    assert status == 200
    assert result["message"] == "Post deleted successfully."

    delete_user("feed_test_user", "ValidPassword1!")


def test_get_feed_for_user_returns_timeline():
    cleanup_user("feed_test_user_one")
    cleanup_user("feed_test_user_two")

    create_user("feed_test_user_one", "feed_test_user_one@example.com", "ValidPassword1!")
    create_user("feed_test_user_two", "feed_test_user_two@example.com", "ValidPassword1!")

    user_one_id = get_user_id("feed_test_user_one")
    user_two_id = get_user_id("feed_test_user_two")

    create_post(
        user_one_id,
        "Mojito",
        5,
        "Older test post",
        "https://example.com/older.jpg",
    )
    create_post(
        user_two_id,
        "Martini",
        5,
        "Newer test post",
        "https://example.com/newer.jpg",
    )

    result, status = get_feed_for_user(user_one_id)

    assert status == 200
    assert isinstance(result, dict)
    assert result["viewer_id"] == user_one_id
    assert "posts" in result
    assert isinstance(result["posts"], list)

    captions = [post.get("caption") for post in result["posts"]]
    assert "Older test post" in captions
    assert "Newer test post" in captions

    delete_user("feed_test_user_one", "ValidPassword1!")
    delete_user("feed_test_user_two", "ValidPassword1!")


def test_get_feed_for_user_includes_username():
    cleanup_user("feed_test_user_three")
    create_user("feed_test_user_three", "feed_test_user_three@example.com", "ValidPassword1!")
    user_id = get_user_id("feed_test_user_three")

    create_post(
        user_id,
        "Negroni",
        5,
        "Post with username in feed",
        "https://example.com/negroni.jpg",
    )

    result, status = get_feed_for_user(user_id)

    assert status == 200
    assert "posts" in result
    assert isinstance(result["posts"], list)

    matching_posts = [
        post for post in result["posts"]
        if post.get("caption") == "Post with username in feed"
    ]

    assert len(matching_posts) >= 1
    assert matching_posts[0]["username"] == "feed_test_user_three"

    delete_user("feed_test_user_three", "ValidPassword1!")


def test_get_feed_for_user_sorted_newest_first():
    cleanup_user("feed_test_user_four")
    cleanup_user("feed_test_user_five")

    create_user("feed_test_user_four", "feed_test_user_four@example.com", "ValidPassword1!")
    create_user("feed_test_user_five", "feed_test_user_five@example.com", "ValidPassword1!")

    user_one_id = get_user_id("feed_test_user_four")
    user_two_id = get_user_id("feed_test_user_five")

    create_post(
        user_one_id,
        "Mojito",
        5,
        "First timeline post",
        "https://example.com/1.jpg",
    )
    create_post(
        user_two_id,
        "Martini",
        5,
        "Second timeline post",
        "https://example.com/2.jpg",
    )

    result, status = get_feed_for_user(user_one_id)

    assert status == 200
    assert "posts" in result
    assert isinstance(result["posts"], list)

    matching_posts = [
        post for post in result["posts"]
        if post.get("caption") in ["First timeline post", "Second timeline post"]
    ]

    assert len(matching_posts) == 2
    returned_order = [post.get("caption") for post in matching_posts]
    assert returned_order == ["Second timeline post", "First timeline post"]

    delete_user("feed_test_user_four", "ValidPassword1!")
    delete_user("feed_test_user_five", "ValidPassword1!")


def test_get_post_by_id_invalid_post_id():
    assert get_post_by_id("invalid_post_id") == ({"error": "Invalid post id."}, 400)


def test_delete_post_invalid_post_id():
    cleanup_user("feed_test_user")
    create_user("feed_test_user", "feed_test_user@example.com", "ValidPassword1!")
    user_id = get_user_id("feed_test_user")

    assert delete_post("invalid_post_id", user_id) == ({"error": "Invalid post id."}, 400)

    delete_user("feed_test_user", "ValidPassword1!")


def test_get_feed_for_user_invalid_user_id():
    assert get_feed_for_user("invalid_user_id") == ({"error": "Invalid user id."}, 400)