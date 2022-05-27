import json
import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger

from .schemas.clients import Client

SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
CLIENTS_PATH = Path(__file__).parent.parent / "instance/clients.json"
try:
    with open(CLIENTS_PATH) as f:
        raw_clients = json.load(f)
except FileNotFoundError:
    logger.warning(
        f"Client file not configured, please configure one at {CLIENTS_PATH}"
    )
    raw_clients = {}
CLIENTS = {client["name"]: Client(**client) for client in raw_clients}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_client(name: str, password: str, clients: dict = CLIENTS):
    client = clients.get(name)
    if not client:
        return False
    if client.password != password:
        return False
    return client


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_name: str = payload.get("sub")
        if client_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    client = CLIENTS.get(client_name)
    if not client:
        raise credentials_exception
    return client
