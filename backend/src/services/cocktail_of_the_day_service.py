from typing import Dict, Any
from src.db import cocktails_collection

def get_random_cocktail() -> Dict[str, Any]:
    """
    Fetches a random cocktail from MongoDB and returns the name and ID.

    Returns:
        Dict[str, Any] A dictionary containing the cocktail's ID and name.
    """

    cocktails = list(cocktails_collection.aggregate([
        {"$sample": {"size": 1}}
    ]))

    if not cocktails:
        raise ValueError("No cocktail data returned from database.")

    cocktail = cocktails[0]

    return {
        "id": cocktail.get("idDrink"),
        "name": cocktail.get("name"),
    }