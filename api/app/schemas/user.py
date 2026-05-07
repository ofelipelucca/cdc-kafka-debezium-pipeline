from pydantic import BaseModel


class UserCreate(BaseModel):
    nome: str
    email: str


class UserResponse(BaseModel):
    guid: str
    nome: str
    email: str
