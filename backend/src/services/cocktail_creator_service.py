from typing import Optional, List, Dict, Any

from src.db import cocktails_collection

# Creates variable with choices for the user to select
def create_cocktail_from_choices(
    flavour: Optional[str] = None,
    ingredient: Optional[str] = None,
    base_spirit: Optional[str] = None,
    alcoholic: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Searches the MongoDB cocktail database based on the user's chosen filters.
    Example: sweet + passion fruit + vodka should return cocktails with these features.
    """

    # MongoDB search through cocktails.
    ask_cocktail: Dict[str, Any] = {}

    # Filter after choosing alcoholoc or non-alcoholic.
    if alcoholic:
        ask_cocktail["alcoholic"] = {"$regex": alcoholic, "$options": "i"}

    # A list for all the ingredient terms.
    ingredient_filters: List[str] = []

    # Adds the chosen ingredient to the list
    if ingredient:
        ingredient_filters.append(ingredient)

    # AAdds the chosen base to the list.
    if base_spirit:
        ingredient_filters.append(base_spirit)

    # Turns flavours into real ingredients.
    flavour_map: Dict[str, List[str]] = {
        "sweet": ["Passion fruit", "Sugar", "Grenadine", "Pineapple juice", "Orange juice", "Vanilla"],
        "sour": ["Lemon juice", "Lime juice"],
        "bitter": ["Bitters", "Campari"],
        "fruity": ["Passion fruit", "Pineapple juice", "Orange juice", "Cranberry juice"],
        "fresh": ["Mint", "Lime juice", "Soda water"],
        "creamy": ["Cream", "Milk", "Baileys"]
    }

    # If user chooses a flavour, add the ingredients with that flavour.
    if flavour:
        ingredient_filters.extend(flavour_map.get(flavour.lower(), [flavour]))

    # Searches for the ingredients.
    if ingredient_filters:
        ask_cocktail["ingredients"] = {
            "$elemMatch": {
                "$regex": "|".join(ingredient_filters),
                "$options": "i"
            }
        }

    # Finds a maximum of 10 cokctails in the MongoDB Database matching the users description.
    results: List[Dict[str, Any]] = list(cocktails_collection.find(ask_cocktail).limit(10))

    # This list will contain the cleaned cocktails we return to the frontend.
    cocktail_results: List[Dict[str, Any]] = []

    # Loop through every MongoDB result and remove unnecessary MongoDB data.
    for cocktail in results:
        cocktail_results.append({
            "id": cocktail.get("idDrink"),
            "name": cocktail.get("name"),
            "category": cocktail.get("category"),
            "alcoholic": cocktail.get("alcoholic"),
            "glass": cocktail.get("glass"),
            "instructions": cocktail.get("instructions"),
            "ingredients": cocktail.get("ingredients"),
            "measurements": cocktail.get("measurements")
        })

    # Returns list of matching cocktails.
    return cocktail_results
