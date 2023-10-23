import os

from app.core import database, config
from typing import List, Dict
import json
import httpx
from functools import reduce
import operator

def apikey():
    return config.config.omdb_apikey

async def _get_page(search :str, page :int):
    # endpoint = "https://www.omdbapi.com/?apikey=a1a0a896&type=movie&s=star+trek&page=1&plot=full"
    endpoint = "https://www.omdbapi.com/"
    params = {
        "apikey": apikey(),
        "type": "movie",
        "plot": "full",
        "s": search,
        "page": page

    }
    async with httpx.AsyncClient() as client:
        r = await client.get(endpoint, params=params)
        bodyj = r.json()
        results = bodyj["Search"]
        return results

async def get_100_movies(search="star trek") -> List[object]:
    search = search.replace(" ", "+")
    movies = [await _get_page(search, page) for page in range(1, 11)]
    movies = reduce(operator.iconcat, movies, [])
    return movies

async def get_movie(imdbID) -> Dict[str, str]:
    # endpoint = "https://www.omdbapi.com/?apikey=a1a0a896&type=movie&s=star+trek&page=1&plot=full"
    endpoint = "https://www.omdbapi.com/"
    params = {
        "apikey": apikey(),
        "type": "movie",
        "plot": "full",
        "i": imdbID,
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(endpoint, params=params)
        movie = r.json()
        return movie

async def get_movie_by_title(title) -> Dict:
    # endpoint = "https://www.omdbapi.com/?apikey=a1a0a896&type=movie&s=star+trek&page=1&plot=full"
    endpoint = "https://www.omdbapi.com/"
    params = {
        "apikey": apikey(),
        "type": "movie",
        "plot": "full",
        "t": title,
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(endpoint, params=params)
        movie = r.json()
        return movie
