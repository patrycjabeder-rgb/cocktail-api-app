from pymongo import MongoClient
import requests
from dotenv import load_dotenv
from pathlib import Path
import os


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

client = MongoClient(os.getenv("MONGO_URI"))

db = client["cocktail_app"]
cocktails_collection = db["cocktails"]


def import_all_cocktails():
    total_count = 0
    for letter in "abcdefghijklmnopqrstuvwxyz":
        count = 0
        print(f"Importing cocktails starting with '{letter}'...")
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data.get('drinks'):
            print(f"No cocktails found starting with '{letter}'.")
            continue

        for cocktail in data['drinks']:
            count += 1
            total_count += 1
            ingredients = []
            measurements = []
            # Loop through the cocktails and extract the ingredients and measuremetns that are not None
            for i in range(1, 16):
                ingredient = cocktail.get(f"strIngredient{i}")

                if ingredient:
                    ingredients.append(ingredient)
                    measurements.append(cocktail.get(f"strMeasure{i}"))
            

            cocktail_info ={
                'idDrink': cocktail['idDrink'],
                'name': cocktail['strDrink'],
                'category': cocktail['strCategory'],
                'alcoholic': cocktail['strAlcoholic'],
                'glass': cocktail['strGlass'],
                'instructions': cocktail['strInstructions'],
                'ingredients': ingredients,
                'measurements': measurements
            }
            cocktails_collection.update_one({'idDrink': cocktail_info['idDrink']}, {'$set': cocktail_info}, upsert=True)
        print(f"Imported {count} cocktails starting with '{letter}'.")
    print(f"Total cocktails imported: {total_count}")
if __name__ == "__main__":
    import_all_cocktails()