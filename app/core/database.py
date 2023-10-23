from google.cloud.firestore_v1 import FieldFilter

from app.core import util

import os
import firebase_admin
from firebase_admin import firestore
# from firebase_admin import credentials
from google.auth import credentials
# from google.cloud import firestore
from google.cloud.client import Client
from google.cloud.firestore_v1.collection import CollectionReference

MOVIES_ID="imdbID"

def get_db() -> Client:
    db = None
    if util.is_test_run():
        # os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
        db = firestore.Client(credentials=credentials.AnonymousCredentials())
    else:
        db = firestore.Client()

    return db

def get_movies_coll() -> CollectionReference:
    db = get_db()
    coll = db.collection("movies")
    return coll

def add_movie(movie):
    get_movies_coll().document(movie[MOVIES_ID]).set(movie)

def get_by_title(title: str):
    movies = get_movies_coll()
    results = movies.where(filter=FieldFilter("Title", "==", title)).stream()
    movie = next(results)
    if movie:
        movie = movie.to_dict()
    return movie

def get_list(page:int=0, size:int=10):
    movies = get_movies_coll()
    start = page * size
    end = start + size
    results = movies.order_by("Title").offset(start).limit(size).stream()
    results = [r.to_dict() for r in results]
    return results
