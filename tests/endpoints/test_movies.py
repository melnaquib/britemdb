import pytest
from fastapi.testclient import TestClient
from app.core.database import get_db, add_movie, get_movies_coll, MOVIES_ID
from app.core.config import config
from app.core import secure

import json

def db_insert_1():
    movies = get_movies_coll()
    db.collection("")
    
def load_file_100():
    entries = []
    with open('tests/movies_star_100.json') as f:
        entries = f.read()
    entries = json.loads(entries)
    return entries

def db_insert_100():
    batch = get_db().batch()
    entries = load_file_100()
    movies_coll = get_movies_coll()
    [add_movie(m)  for m in entries]
    batch.commit()
    return entries

def db_insert_10():
    batch = get_db().batch()
    entries = load_file_10()
    movies_coll = get_movies_coll()
    [add_movie(m)  for m in entries]
    batch.commit()
    return entries

async def db_clear():
    batch = get_db().batch()
    async for m in get_movies_coll().stream():
        await m.reference.delete()
    await batch.commit()

@pytest.fixture
async def user1():
    user = {
        "username": config.users_1_username,
        "password": config.users_1_password,
        "roles": {
            "can_delete": config.users_1_can_delete
        }
    }
    return user

@pytest.fixture
async def token1_header(user1, client: TestClient):
    response = client.post(secure.TOKEN_URL, data=user1)
    token = response.json()["access_token"]
    header = {"Authorization": f"Bearer {token}"}
    return header

async def test_get(client: TestClient):
    entries = db_insert_100()
    movie = entries[2]
    res = client.get('/movies/' + movie["imdbID"])

    assert res.status_code == 200
    assert movie == res.json()

async def test_get_by_title(client: TestClient):
    entries = db_insert_100()
    movie = entries[2]
    res = client.get('/movies/by-title/' + movie["Title"])

    assert res.status_code == 200
    assert movie == res.json()

async def test_get_list(client: TestClient):
    entries = db_insert_100()
    path = '/movies/?page=5&size=15'
    res1 = client.get(path).json()
    assert 15 == len(res1)
    res2 = client.get(path).json()
    assert res1 == res2

async def test_add(client: TestClient):
    test_movie = {
        "imdbID": "tt0087332",
        "Title": "Ghostbusters",
    }
    count_before = get_movies_coll().count().get()[0][0].value
    res = client.post('/movies/' + test_movie["imdbID"])
    assert res.status_code == 200
    assert test_movie["Title"] == res.json()["Title"]
    count_after = get_movies_coll().count().get()[0][0].value
    assert (count_before + 1) == count_after

async def test_add_by_title(client: TestClient):
    test_movie = {
        "imdbID": "tt0078346",
        "Title": "Superman",
    }
    count_before = get_movies_coll().count().get()[0][0].value
    res = client.post('/movies/by-title/' + test_movie["Title"])
    assert res.status_code == 200
    assert test_movie["imdbID"] == res.json()["imdbID"]
    count_after = get_movies_coll().count().get()[0][0].value
    assert (count_before + 1) == count_after

async def test_delete(client: TestClient, token1_header):
    entries = db_insert_100()
    count_before = get_movies_coll().count().get()[0][0].value
    movie = entries[2]
    res = client.delete('/movies/' + movie["imdbID"], headers=token1_header)
    assert res.status_code == 200
    count_after = get_movies_coll().count().get()[0][0].value
    assert (count_before - 1) == count_after
