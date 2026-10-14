from src.db import cocktails_collection, posts_collection
import random

def search_cocktail_by_name(name: str) -> dict:
    ''' Search for a cocktail by name using the MongoDB collection.'''
    cocktail = cocktails_collection.find_one(
        {"name": {"$regex": f"^{name}$", "$options": "i"}}
    )

    if not cocktail:
        return None

    cocktail.pop("_id", None)

    return cocktail

def search_cocktail_by_ingredient(ingredient: str) -> list:
    ''' Search for cocktails by ingredient using the MongoDB collection.'''
    cocktails = list(
        cocktails_collection.find(
        {"ingredients": {"$regex": f"^{ingredient}$", "$options": "i"}}, {"_id": 0, 'idDrink': 1, 'name': 1})
    )
        
    return cocktails

def search_cocktail_by_multiple_ingredients(ingredients: list) -> list:
    ''' Search for cocktails that contain all of the specified ingredients using the MongoDB collection.'''
    
    cocktails = list(
        cocktails_collection.find(
        {"ingredients": {"$all": ingredients}}, {"_id": 0, 'idDrink': 1, 'name': 1})
    )
        
    return cocktails

def get_average_rating(cocktail_name: str) -> float:
    ''' Calculate the average rating for a cocktail based on user reviews.'''
    result = list(posts_collection.aggregate([
        {"$match": {"cocktail_name": cocktail_name}},
        {"$group": {"_id": None, "average_rating": {"$avg": "$review_score"}, "review_count": {"$sum": 1}}}
    ]))

    if not result:
        return {"average_rating": 0, "review_count": 0}

    return {"average_rating": round(result[0]["average_rating"], 2), "review_count": result[0]["review_count"]}

def get_cocktail_by_id(cocktail_id: str) -> dict:
    ''' Search for a cocktail by its ID using the MongoDB collection.'''
    cocktail = cocktails_collection.find_one({"idDrink": cocktail_id})

    if not cocktail:
        return None

    rating_info = get_average_rating(cocktail["name"])

    cocktail["average_rating"] = rating_info["average_rating"]
    cocktail["review_count"] = rating_info["review_count"]

    cocktail.pop("_id", None)

    return cocktail

# Mood to cocktail mapping for the suggest_cocktail_by_mood function
MOOD_COCKTAILS = {
    "happy": [
        "Margarita",
        "Mojito",
        "Tequila Sunrise"
    ],

    "relaxed": [
        "White Russian",
        "Irish Coffee",
        "Hot Toddy"
    ],

    "party": [
        "Long Island Iced Tea",
        "Sex on the Beach",
        "Zombie"
    ],

    "romantic": [
        "Cosmopolitan",
        "French Martini",
        "Bellini"
    ],

    "adventurous": [
        "Mai Tai",
        "Negroni",
        "Singapore Sling"
    ],

    "celebratory": [
        "Champagne Cocktail",
        "Kir Royale",
        "Mimosa"
    ],

    "sophisticated": [
        "Martini",
        "Manhattan",
        "Old Fashioned"
    ],

    "stressed": [
        "Hot Toddy",
        "White Russian",
        "Brandy Alexander"
    ],

    "tropical": [
        "Piña Colada",
        "Blue Hawaiian",
        "Bahama Mama"
    ],

    "energetic": [
        "Espresso Martini",
        "Vodka Red Bull",
        "Irish Coffee"
    ]
}

def suggest_cocktail_by_mood(mood: str) -> dict:
    ''' Suggest a cocktail based on the user's mood.'''
    if mood not in MOOD_COCKTAILS:
        return None
    
    cocktails = MOOD_COCKTAILS.get(mood.lower())
    if not cocktails:
        return None

    suggested_cocktail = random.choice(cocktails)
    
    return cocktails_collection.find_one({"name": suggested_cocktail}, {"_id": 0})

