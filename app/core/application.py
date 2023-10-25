from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from app.api.endpoints import movies
from app.core import secure, database

from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

def create_api():
    api = FastAPI()

    @api.on_event("startup")
    async def startup_event():
        await database.initdb()

    @api.get("/")
    async def redirect_typer():
        return RedirectResponse("/docs/")

    api.include_router(secure.router)
    api.include_router(movies.router)

    return api
