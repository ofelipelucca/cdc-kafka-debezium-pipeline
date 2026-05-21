from uuid import UUID, uuid4
from typing import Optional
from pydantic import ValidationError

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserDTO
from app.exceptions.user_exceptions import InvalidEmailFormatException


class UserService:
    def __init__(self, db):
        self.user_repository = UserRepository(db=db)

    def create_user(self, user_create: UserCreate) -> UserDTO:
        try:
            user_dto = UserDTO(guid=uuid4(), nome=user_create.nome, email=user_create.email)
        except ValidationError:
            raise InvalidEmailFormatException()

        return self.user_repository.create_user(new_user=user_dto)

    def get_user_by_guid(self, guid: UUID) -> Optional[UserDTO]:
        user = self.user_repository.get_user_by_guid(guid)

        if not user:
            return None

        return UserDTO(guid=user.guid, nome=user.nome, email=user.email)