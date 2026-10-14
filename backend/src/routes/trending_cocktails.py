from flask import Blueprint, jsonify, Response

from src.services.trending_cocktails_service import (
    get_trending_cocktails
)

trending_cocktails_bp = Blueprint("trending_cocktails", __name__)


@trending_cocktails_bp.route("/trending-cocktails", methods=["GET"])
def trending_cocktails() -> Response:
    """
    Endpoint to retrieve the top 5 trending cocktails based on user posts.
    """

    try:
        trending_cocktails = get_trending_cocktails()
        return jsonify(trending_cocktails), 200

    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500