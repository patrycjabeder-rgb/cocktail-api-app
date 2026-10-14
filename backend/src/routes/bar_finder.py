from flask import Blueprint, jsonify, request

from src.services.bar_finder_service import search_bars

bar_finder_bp = Blueprint("bar_finder", __name__)

@bar_finder_bp.route("/bar-finder", methods=["GET"])
def get_bars():
    """Search bars by city with optional filters."""
    home_city = request.args.get("home_city", "").strip()
    name = request.args.get("name", "").strip()
    price = request.args.get("price", "").strip()

    rating_raw = request.args.get("rating", "").strip()
    rating = None

    if rating_raw:
        try:
            rating = float(rating_raw)
        except ValueError:
            return jsonify({"error": "rating must be a valid number."}), 400

    result, status = search_bars(
        home_city=home_city,
        name=name,
        rating=rating,
        price=price or None
    )

    return jsonify(result), status