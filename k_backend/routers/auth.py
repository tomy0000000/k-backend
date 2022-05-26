from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import authenticate_client, create_access_token, get_client
from ..schemas import clients

tag = {
    "name": "Authorization",
    "description": "Authenticate and verify permissions",
}

router = APIRouter(
    tags=[tag["name"]],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=clients.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    client = authenticate_client(form_data.username, form_data.password)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect client name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": client.name})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/client", response_model=clients.Client)
async def check_auth(client: clients.Client = Depends(get_client)):
    return client
