from flask import Blueprint, jsonify, Response
from typing import Optional, Dict, Any, List

from src.services.cocktail_creator_service import create_cocktail_from_choices

cocktail_creator_bp = Blueprint("cocktail_creator", __name__)

from flask import Blueprint, jsonify, request

@cocktail_creator_bp.route("/create-cocktail", methods=["GET", "POST"])

def create_cocktail() -> Response:
    """Cocktail creator tool based on preferences."""

    try:
        # Reads the JSON send by the user
        user_choices: Dict[str, Any] = request.get_json() or {}

        flavour: Optional[str] = user_choices.get("flavour")
        ingredient: Optional[str] = user_choices.get("ingredient")
        base_spirit: Optional[str] = user_choices.get("base_spirit")
        alcoholic: Optional[str] = user_choices.get("alcoholic")

        matching_cocktails: List[Dict[str, Any]] = create_cocktail_from_choices(
            flavour=flavour,
            ingredient=ingredient,
            base_spirit=base_spirit,
            alcoholic=alcoholic
        )

        # If there are no matching cocktails, return message.
        if not matching_cocktails:
            return jsonify({
                "message": "No matching cocktails found. Try different ingredients or flavours."
            }), 404

        # Return the user's choices and the matching cocktails.
        return jsonify({
            "user_choices": user_choices,
            "matches": matching_cocktails
        }), 200

    except Exception as e:
        # Return a server error if something goes wrong.
        return jsonify({
            "error": "An internal server error occurred.",
            "details": str(e)
        }), 500