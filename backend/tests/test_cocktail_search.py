import pytest
from backend.src.services.search_cocktail_service import get_average_rating, search_cocktail_by_name, search_cocktail_by_ingredient, search_cocktail_by_multiple_ingredients, get_cocktail_by_id, suggest_cocktail_by_mood

def test_search_cocktail_by_name():
    # Test searching for a cocktail by name
    cocktail = search_cocktail_by_name("Margarita")
    assert cocktail is not None
    assert cocktail['name'] == "Margarita"

def test_search_cocktail_by_ingredient():
    # Test searching for cocktails by ingredient
    cocktails = search_cocktail_by_ingredient("Tequila")

    assert isinstance(cocktails, list)
    assert len(cocktails) > 0
    assert all("name" in cocktail for cocktail in cocktails)
    assert all("idDrink" in cocktail for cocktail in cocktails)

def test_search_cocktail_by_multiple_ingredients():
    # Test searching for cocktails by multiple ingredients
    cocktails = search_cocktail_by_multiple_ingredients(["Tequila", "Lime juice"])

    assert isinstance(cocktails, list)
    assert len(cocktails) > 0
    assert all("name" in cocktail for cocktail in cocktails)
    assert all("idDrink" in cocktail for cocktail in cocktails)
    
def test_get_cocktail_by_id():
    # Test retrieving a cocktail by its ID
    cocktail = get_cocktail_by_id("11007")
    assert cocktail is not None
    assert cocktail['idDrink'] == "11007"

def test_get_cocktail_by_id_not_found():
    # Test retrieving a cocktail by its ID when it doesn't exist
    cocktail = get_cocktail_by_id("99999")
    assert cocktail is None

def test_suggest_cocktail_by_mood():
    # Test suggesting a cocktail based on mood
    suggested_cocktail = suggest_cocktail_by_mood("happy")
    assert suggested_cocktail is not None
    assert suggested_cocktail['name'] in ["Margarita", "Mojito", "Tequila Sunrise"]

def test_suggest_cocktail_by_mood_not_found():
    # Test suggesting a cocktail based on a mood with no suggestions
    suggested_cocktail = suggest_cocktail_by_mood("nonexistent")
    assert suggested_cocktail is None

def test_suggest_cocktail_by_mood_empty():
    # Test suggesting a cocktail based on an empty mood
    suggested_cocktail = suggest_cocktail_by_mood("")
    assert suggested_cocktail is None

def test_get_average_rating():
    # Test calculating the average rating for a cocktail
    rating_info = get_average_rating("Margarita")
    assert isinstance(rating_info, dict)
    assert "average_rating" in rating_info
    assert "review_count" in rating_info