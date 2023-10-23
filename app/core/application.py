from fastapi.security import OAuth2PasswordRequestForm

from app.api.endpoints import movies
from app.core import secure

from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

def create_api():
    api = FastAPI()

    api.include_router(secure.router)
    api.include_router(movies.router)

    return api
