from flask import Blueprint, Flask, jsonify, request

from src.services.search_cocktail_service import (
    search_cocktail_by_name,
    search_cocktail_by_ingredient,
    search_cocktail_by_multiple_ingredients,
    get_cocktail_by_id, suggest_cocktail_by_mood, get_average_rating
)

from src.db import posts_collection

search_cocktails_bp = Blueprint("search_cocktails", __name__)

@search_cocktails_bp.route("/search-cocktail-name", methods=["GET"])
def search_cocktail_name():
    '''Endpoint to search for a cocktail by name. Expects a query parameter "name".'''
    name = request.args.get('name')
    
    if not name:
        return jsonify({'error': 'No name provided.'}), 400
    
    cocktail_info = search_cocktail_by_name(name)
    
    if not cocktail_info:
        return jsonify({'error': 'Cocktail not found'}), 404
    
    return jsonify(cocktail_info), 200

@search_cocktails_bp.route('/search-cocktail-ingredient', methods=['GET'])
def search_cocktail_ingredient():
    '''Endpoint to search for cocktails by ingredient. Expects a query parameter "ingredient".'''
    
    ingredient = request.args.get('ingredient')
    
    if not ingredient:
        return jsonify({'error': 'No ingredient provided.'}), 400
    
    cocktails_info = search_cocktail_by_ingredient(ingredient)
    
    if not cocktails_info:
        return jsonify({'error': 'No cocktails found with the given ingredient'}), 404
    
    return jsonify(cocktails_info), 200

@search_cocktails_bp.route('/search-cocktail-multiple-ingredients', methods=['GET'])
def search_cocktail_multiple_ingredients():
    '''Endpoint to search for cocktails by multiple ingredients. Expects a query parameter "ingredients" which is a comma-separated list of ingredients.'''
    
    ingredients_string = request.args.get('ingredients')
    
    if not ingredients_string:
        return jsonify({'error': 'No ingredients provided.'}), 400

    ingredients = [
    ingredient.strip().capitalize()
    for ingredient in ingredients_string.split(',')
]

    if not ingredients:
        return jsonify({'error': 'No ingredients provided.'}), 400
    
    
    cocktails_info = search_cocktail_by_multiple_ingredients(ingredients)
    
    if not cocktails_info:
        return jsonify({'error': 'No cocktails found with the given ingredients'}), 404
    
    return jsonify(cocktails_info), 200

@search_cocktails_bp.route('/cocktail-by-id', methods=['GET'])
def get_cocktail_by_id_endpoint():
    '''Endpoint to get a cocktail by its ID. Expects a query parameter "id_drink".'''
    cocktail_id = request.args.get('id_drink')

    if not cocktail_id:
        return jsonify({'error': 'No cocktail ID provided.'}), 400

    cocktail_info = get_cocktail_by_id(cocktail_id)

    if not cocktail_info:
        return jsonify({'error': 'Cocktail not found'}), 404

    return jsonify(cocktail_info), 200

@search_cocktails_bp.route('/cocktail-by-mood', methods=['GET'])
def suggest_cocktail_by_mood_endpoint():
    '''Endpoint to suggest a cocktail based on the user's mood. Expects a query parameter "mood".'''
    mood = request.args.get('mood')

    if not mood:
        return jsonify({'error': 'No mood provided.'}), 400

    suggested_cocktail = suggest_cocktail_by_mood(mood)

    if not suggested_cocktail:
        return jsonify({'error': 'No cocktail found for the given mood'}), 404

    return jsonify(suggested_cocktail), 200

@search_cocktails_bp.route('/cocktail-rating', methods=['GET'])
def get_cocktail_rating():

    cocktail_name = request.args.get("cocktail_name")

    if not cocktail_name:
        return jsonify({"error": "No cocktail name provided."}), 400

    return jsonify(get_average_rating(cocktail_name)), 200