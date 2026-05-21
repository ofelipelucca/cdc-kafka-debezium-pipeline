from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    guid: UUID
    nome: str
    email: EmailStr

class UserCreate(BaseModel):
    nome: str
    email: EmailStr

class UserResponse(UserDTO):
    pass