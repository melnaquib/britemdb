from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.application import create_api
from app.core.database import get_db, get_movies_coll, add_movie
from app.core import omdb

import json

def load_file_100():
    entries = []
    with open('tests/movies_star_100.json') as f:
        entries = f.read()
    entries = json.loads(entries)
    return entries

@pytest.fixture(scope='function')
def db_insert_100():
    batch = get_db().batch()
    entries = load_file_100()
    movies_coll = get_movies_coll()
    [add_movie(m)  for m in entries]
    batch.commit()
    return entries

async def db_clear():
    batch = get_db().batch()
    async for m in get_movies_coll().stream():
        await m.reference.delete()
    await batch.commit()

@pytest.fixture(scope='module')
def client() -> Generator:
    api = create_api()
    with TestClient(api) as c:
        yield c
