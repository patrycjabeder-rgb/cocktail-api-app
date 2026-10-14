import os
from pathlib import Path
from typing import Any
import serpapi

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

def bar_name_search(name: str | None) -> str:
    """Optional search for specific bar name/ particular feature or a bar (e.g. pool bar, modern, cozy etc.)."""
    search_keywords = name.split()

    filtered_words = []
    for word in search_keywords:
        if word != "bar":
            filtered_words.append(word)

    search_keywords = filtered_words
    name = " ".join(search_keywords)

    if name == "":
        return ""

    if not name.replace(" ", "").isalpha():
        raise ValueError("Please use letters only.")

    return name

def price_range_search(price: str | None) -> str | None:
    """Optional search for price range for the bar."""
    price_options = {
        "1": "cheap",
        "2": "moderate",
        "3": "expensive",
        "4": "very expensive"
    }

    if not price:
        return None

    price = price.strip()

    if price == "":
        return ""

    if price not in price_options:
        raise ValueError("Please must be: 1, 2, 3, or 4.")

    return price

def bar_rating_search(rating: float | None) -> float:
    """Optional search for the bar rating."""
    if rating is None:
        return 2.0

    rating = float(rating)

    if rating < 2.0:
        rating = 2.0
    elif rating > 4.5:
        rating = 4.5

    rating = round(rating * 2) / 2
    return rating

def get_home_city(home_city: str) -> str:
    """The city which the app searches for bars."""
    home_city = home_city.strip().title()

    if not home_city:
        raise ValueError("Home city is required.")

    if not home_city.replace(" ", "").isalpha():
        raise ValueError("Home city must have letters only.")

    return home_city

def search_bars(
    home_city: str,
    name: str = "",
    rating: float | None = None,
    price: str | None = None
) -> tuple[dict[str, Any], int]:
    """Search bars in a city using SerpAPI."""
    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        return {"error": "SERPAPI_API_KEY is missing."}, 500

    try:
        user_search = bar_name_search(name or "")
        home_city = get_home_city(home_city)
        rating = bar_rating_search(rating)
        price_range = price_range_search(price)
    except ValueError as e:
        return {"error": str(e)}, 400

    client = serpapi.Client(api_key=api_key)

    results = client.search({
        "engine": "google_maps",
        "q": f"{user_search} bar" if user_search else "bar",
        "location": f"{home_city}",
        "google_domain": "google.com",
        "gl": "nl",
        "hl": "en",
        "z": 20,
        "nearby": True,
        "rating": f"{rating}"
    })

    local_results = results.get("local_results", [])
    filtered_results = []

    for item in local_results:
        item_rating = item.get("rating")
        item_price = item.get("price")

        try:
            if item_rating is None or float(item_rating) < rating:
                continue
        except (TypeError, ValueError):
            continue

        if price_range not in ("", None) and str(item_price) != price_range:
            continue

        #Adds (almost) all result types so the app can filter through them later if needed.
        filtered_results.append({
            "name": item.get("title"),
            "address": item.get("address"),
            "rating": item.get("rating"),
            "reviews": item.get("reviews"),
            "price": item.get("price"),
            "type": item.get("type"),
            "open_state": item.get("open_state"),
            "hours": item.get("hours"),
            "phone": item.get("phone"),
            "website": item.get("website"),
            "gps_coordinates": item.get("gps_coordinates")
        })

    return {
        "query": f"{user_search} bar" if user_search else "bar",
        "city": home_city,
        "count": len(filtered_results),
        "results": filtered_results
    }, 200