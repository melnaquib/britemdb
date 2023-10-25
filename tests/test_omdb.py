import pytest

from app.core.omdb import get_100_movies


# @pytest.mark.skip()
async def test_get_100():
    movies = await get_100_movies("star")
    assert len(movies) == 100
