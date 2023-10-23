from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.logger import logger
from app.core.database import get_movies_coll, add_movie, get_by_title as get_movie_by_title, get_list as get_movies_list
from app.core import omdb
from app.core.secure import permission, manager

import os

router = APIRouter(prefix="/movies")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get('/{imdbID}')
def get(imdbID :str):
    movies = get_movies_coll()
    movie = movies.document(imdbID).get()
    if movie.exists:
        return movie.to_dict()
    raise HTTPException(status_code=404, detail="Movie not found")

@router.get('/by-title/{title}')
def get_by_title(title: str):
    movie = get_movie_by_title(title)
    if movie:
        return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@router.get('/')
def get_list(page:int=0, size:int=10):
    movies = get_movies_list(page, size)
    if movies:
        return movies
    raise HTTPException(status_code=404, detail="Movie not found")

@router.post('/{imdbID}')
async def add(imdbID :str):
    movie = await omdb.get_movie(imdbID)
    if movie:
        add_movie(movie)
        return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@router.post('/by-title/{title}')
async def add_by_title(title :str):
    movie = await omdb.get_movie_by_title(title)
    if movie:
        add_movie(movie)
        return movie
    raise HTTPException(status_code=404, detail="Movie not found")

# def delete(imdbID :str, user=Depends(manager)):
@router.delete('/{imdbID}')
@permission("can_delete")
def delete(imdbID :str, user=Depends(manager), ):
    movies = get_movies_coll()
    movie = movies.document(imdbID)
    if movie.get().exists:
        movie.delete()
        return {}
    raise HTTPException(status_code=404, detail="Movie not found")
