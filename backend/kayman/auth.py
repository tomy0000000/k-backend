import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger

from kayman.core.config import settings
from kayman.schemas.clients import Client

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


def authenticate_client(
    name: str, password: str, clients: dict[str, Client] = CLIENTS
) -> Client | None:
    client = clients.get(name)
    if not client:
        return None
    if client.password != password:
        return None
    return client


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_client(token: str = Depends(oauth2_scheme)) -> Client:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        client_name = payload.get("sub")
        if client_name is None:
            raise credentials_exception
    except JWTError as err:
        raise credentials_exception from err
    client = CLIENTS.get(client_name)
    if not client:
        raise credentials_exception
    return client
