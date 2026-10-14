import pytest

import src.services.bar_finder_service as bar_service

from src.services.bar_finder_service import (
    bar_name_search,
    price_range_search,
    bar_rating_search,
    get_home_city,
    search_bars
)

# bar_name_search tests
def test_bar_name_search_empty():
    '''
    Test that bar_name_search returns an empty string when no name is given.
    '''
    assert bar_name_search("") == ""


def test_bar_name_search_removes_bar_word():
    '''
    Test that bar_name_search removes the word "bar" from the search.
    '''
    assert bar_name_search("cocktail bar") == "cocktail"
    assert bar_name_search("sports bar") == "sports"


def test_bar_name_search_invalid_characters():
    '''
    Test that bar_name_search rejects non-letter characters.
    '''
    with pytest.raises(ValueError, match="Please use letters only."):
        bar_name_search("bar123")


# price_range_search tests
def test_price_range_search_empty():
    '''
    Test that price_range_search allows empty input.
    '''
    assert price_range_search("") is None
    assert price_range_search(None) is None


def test_price_range_search_valid():
    '''
    Test that price_range_search accepts values 1 to 4.
    '''
    assert price_range_search("1") == "1"
    assert price_range_search("2") == "2"
    assert price_range_search("3") == "3"
    assert price_range_search("4") == "4"


def test_price_range_search_invalid():
    '''
    Test that price_range_search rejects invalid values.
    '''
    with pytest.raises(ValueError, match="Please must be: 1, 2, 3, or 4."):
        price_range_search("5")


# bar_rating_search tests
def test_bar_rating_search_default():
    '''
    Test that bar_rating_search defaults to 2.0 when no rating is given.
    '''
    assert bar_rating_search(None) == 2.0


def test_bar_rating_search_clamps_range():
    '''
    Test that bar_rating_search clamps values into the allowed range.
    '''
    assert bar_rating_search(1.0) == 2.0
    assert bar_rating_search(5.0) == 4.5


def test_bar_rating_search_rounds_to_half():
    '''
    Test that bar_rating_search rounds to the nearest 0.5.
    '''
    assert bar_rating_search(3.2) == 3.0
    assert bar_rating_search(3.3) == 3.5


# get_home_city tests
def test_get_home_city_valid():
    '''
    Test that get_home_city formats the city correctly.
    '''
    assert get_home_city("amsterdam") == "Amsterdam"


def test_get_home_city_empty():
    '''
    Test that get_home_city rejects empty input.
    '''
    with pytest.raises(ValueError, match="Home city is required."):
        get_home_city("")


def test_get_home_city_invalid():
    '''
    Test that get_home_city rejects invalid characters.
    '''
    with pytest.raises(ValueError, match="Home city must have letters only."):
        get_home_city("Amst3rdam")


# search_bars tests
def test_search_bars_missing_api_key(monkeypatch):
    '''
    Test that search_bars returns an error when the API key is missing.
    '''
    monkeypatch.setattr(bar_service.os, "getenv", lambda key: None)

    assert search_bars("Amsterdam") == (
        {"error": "SERPAPI_API_KEY is missing."},
        500
    )


def test_search_bars_invalid_city(monkeypatch):
    '''
    Test that search_bars returns an error for an invalid city.
    '''
    monkeypatch.setattr(bar_service.os, "getenv", lambda key: "fake_key")

    assert search_bars("") == (
        {"error": "Home city is required."},
        400
    )


def test_search_bars_success(monkeypatch):
    '''
    Test that search_bars returns filtered bar results.
    '''
    monkeypatch.setattr(bar_service.os, "getenv", lambda key: "fake_key")

    class MockClient:
        def __init__(self, api_key):
            self.api_key = api_key

        def search(self, params):
            return {
                "local_results": [
                    {
                        "title": "Bar One",
                        "address": "Amsterdam Center",
                        "rating": 4.5,
                        "reviews": 120,
                        "price": "2",
                        "type": "Bar",
                        "open_state": "Open",
                        "hours": "10:00-23:00",
                        "phone": "123456789",
                        "website": "https://barone.example.com",
                        "gps_coordinates": {"latitude": 52.37, "longitude": 4.89}
                    },
                    {
                        "title": "Bar Two",
                        "address": "Amsterdam West",
                        "rating": 3.0,
                        "price": "1"
                    }
                ]
            }

    monkeypatch.setattr(bar_service.serpapi, "Client", MockClient)

    result, status = search_bars(
        home_city="Amsterdam",
        name="cocktail",
        rating=4.0,
        price="2"
    )

    assert status == 200
    assert result["city"] == "Amsterdam"
    assert result["count"] == 1
    assert result["results"][0]["name"] == "Bar One"