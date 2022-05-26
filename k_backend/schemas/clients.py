from pydantic import BaseModel


class Client(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
