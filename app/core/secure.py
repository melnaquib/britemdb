from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException

from app.api.endpoints import movies
from app.core.config import config, Config

from typing import Annotated, Dict, Union, Optional, List
from fastapi import FastAPI, Depends
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

from functools import partial, wraps

TOKEN_URL = "/token"
router = APIRouter()
manager = LoginManager(config.secret, TOKEN_URL)

def preconf_user():
    user = {
        "username": config.users_1_username,
        "password": config.users_1_password,
        "roles": {
            "can_delete": config.users_1_can_delete
        }
    }
    return user

def user_auth(username, password):
    # TODO, user management
    user = preconf_user()
    success = username == user["username"] and password == user["password"]
    if success:
        del user["password"]
        return user
    else:
        return None

from pydantic import BaseModel
class LoginRsp(BaseModel):
    access_token: str
    token_type: str

@router.post(TOKEN_URL, response_model=Dict[str, str])
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    username, password = data.username, data.password
    user = user_auth(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = manager.create_access_token(data=dict(sub=user["username"],
                                                         can_delete=user["roles"]["can_delete"]))
    rsp = {'access_token': access_token, 'token_type': 'bearer'}
    return rsp

@manager.user_loader()
def get_user(username: str):
    user = preconf_user()
    return user if user["username"] == username else None

def has_perm(perm :str, user):
    if not user or "roles" not in user or perm not in user["roles"] or not user["roles"][perm]:
        raise HTTPException(status_code=403, detail="Not Authorized To " + perm)

def has_perms(perms :List[str], user):
    if type(perms) is str:
        perms = [perms]
    for perm in perms:
        has_perm(perm, user)

def permission(perms: Union[str, List[str]]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(user=Depends(manager), *args, **kwargs):
            has_perms(perms, user)
            return fn(*args, **kwargs)
        return wrapper
    return decorator