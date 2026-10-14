import pytest
from backend.src.services.trending_cocktails_service import get_trending_cocktails

def test_get_trending_cocktails():
    # Test retrieving the top 5 trending cocktails
    trending_cocktails = get_trending_cocktails()

    assert isinstance(trending_cocktails, list)
    assert len(trending_cocktails) <= 5
    assert all("cocktail_name" in cocktail for cocktail in trending_cocktails)
    assert all("post_count" in cocktail for cocktail in trending_cocktails)

