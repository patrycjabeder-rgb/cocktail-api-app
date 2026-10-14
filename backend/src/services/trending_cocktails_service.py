from src.db import posts_collection
from typing import Any

def get_trending_cocktails() -> list[dict[str, Any]]:
    """
    Fetches the top 5 most frequently posted cocktails.

    Returns:
        list[dict[str, Any]]: A list of cocktails and their post counts.
    """

    return list(
        posts_collection.aggregate([
            {
                "$group": {
                    "_id": "$cocktail_name",
                    "post_count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "post_count": -1
                }
            },
            {
                "$limit": 5
            },
            {
                "$project": {
                    "_id": 0,
                    "cocktail_name": "$_id",
                    "post_count": 1
                }
            }
        ])
    )