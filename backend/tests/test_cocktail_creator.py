from typing import Any, Dict, List

import pytest
from flask import Flask

from src.routes.cocktail_creator import cocktail_creator_bp
import src.services.cocktail_creator_service as cocktail_service


class FakeCursor:
    def __init__(self, cocktails: List[Dict[str, Any]]):
        self.cocktails = cocktails

    def limit(self, number: int) -> List[Dict[str, Any]]:
        return self.cocktails[:number]

class FakeCollection:
    def __init__(self, cocktails: List[Dict[str, Any]]):
        self.cocktails = cocktails

    def find(self, query: Dict[str, Any]) -> FakeCursor:
        return FakeCursor(self.cocktails)


def get_test_cocktail() -> Dict[str, Any]:
    return {
        "_id": "mongodb_id_should_not_be_returned",
        "idDrink": "17222",
        "name": "Passion Fruit Martini",
        "category": "Cocktail",
        "alcoholic": "Alcoholic",
        "glass": "Cocktail glass",
        "instructions": "Shake all ingredients with ice and strain into a glass.",
        "ingredients": ["Vodka", "Passion fruit", "Lime juice", "Sugar"],
        "measurements": ["50ml", "25ml", "15ml", "10ml"]
    }


def use_fake_database(cocktails: List[Dict[str, Any]]) -> None:
    cocktail_service.cocktails_collection = FakeCollection(cocktails)


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(cocktail_creator_bp)

    with app.test_client() as client:
        yield client


def test_create_cocktail_from_choices_returns_one_cocktail():
    use_fake_database([get_test_cocktail()])

    results = cocktail_service.create_cocktail_from_choices(
        flavour="sweet",
        ingredient="Passion fruit",
        base_spirit="Vodka",
        alcoholic="Alcoholic"
    )

    assert len(results) == 1
    assert results[0]["name"] == "Passion Fruit Martini"


def test_create_cocktail_from_choices_returns_clean_data():
    use_fake_database([get_test_cocktail()])

    results = cocktail_service.create_cocktail_from_choices(
        flavour="sweet",
        ingredient="Passion fruit",
        base_spirit="Vodka",
        alcoholic="Alcoholic"
    )

    assert results[0]["id"] == "17222"
    assert "_id" not in results[0]


def test_post_request_returns_status_code_200(client):
    use_fake_database([get_test_cocktail()])

    response = client.post(
        "/create-cocktail",
        json={
            "flavour": "sweet",
            "ingredient": "Passion fruit",
            "base_spirit": "Vodka",
            "alcoholic": "Alcoholic"
        }
    )

    assert response.status_code == 200


def test_post_request_returns_matching_cocktail(client):
    use_fake_database([get_test_cocktail()])

    response = client.post(
        "/create-cocktail",
        json={
            "flavour": "sweet",
            "ingredient": "Passion fruit",
            "base_spirit": "Vodka",
            "alcoholic": "Alcoholic"
        }
    )

    data = response.get_json()

    assert data is not None
    assert data["matches"][0]["name"] == "Passion Fruit Martini"
    assert data["matches"][0]["alcoholic"] == "Alcoholic"


def test_post_request_returns_404_when_no_cocktails_found(client):
    use_fake_database([])

    response = client.post(
        "/create-cocktail",
        json={
            "flavour": "sour",
            "ingredient": "Banana",
            "base_spirit": "Rum",
            "alcoholic": "Alcoholic"
        }
    )

    data = response.get_json()

    assert response.status_code == 404
    assert data is not None
    assert data["message"] == "No matching cocktails found. Try different ingredients or flavours."
