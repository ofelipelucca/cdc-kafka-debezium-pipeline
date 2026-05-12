from pydantic import BaseModel


class UserDTO(BaseModel):
    guid: str
    nome: str
    email: str

class UserCreate(BaseModel):
    nome: str
    email: str

class UserResponse(UserDTO):
    pass