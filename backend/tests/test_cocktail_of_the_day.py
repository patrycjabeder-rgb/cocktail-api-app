import pytest
from backend.src.services.cocktail_of_the_day_service import get_random_cocktail

def test_get_random_cocktail():
    cocktail = get_random_cocktail()
    assert cocktail is not None
    assert "id" in cocktail
    assert "name" in cocktail