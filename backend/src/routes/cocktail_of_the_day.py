from flask import Blueprint, jsonify, request, Response
import requests

from src.services.cocktail_of_the_day_service import (
    get_random_cocktail
)

cocktail_of_the_day_bp = Blueprint("cocktail_of_the_day", __name__)

@cocktail_of_the_day_bp.route('/cocktail-of-the-day', methods=['GET'])
def get_cocktail_of_the_day() -> Response:
    """
    RESTful endpoint to retrieve the daily featured cocktail.
    Uses meaningful nouns and correct HTTP method.
    """
    try:
        cocktail_data = get_random_cocktail()
        return jsonify(cocktail_data), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to retrieve data from external cocktail service.",
            "details": str(e)
        }), 502
        
    except Exception as e:
        return jsonify({
            "error": "An internal server error occurred.",
            "details": str(e)
        }), 500