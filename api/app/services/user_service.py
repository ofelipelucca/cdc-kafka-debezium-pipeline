import uuid
from typing import Optional

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserDTO


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_create: UserCreate) -> UserDTO:
        user_dto = UserDTO(guid=str(uuid.uuid4()), nome=user_create.nome, email=user_create.email)

        return self.user_repository.create_user(new_user=user_dto)

    def get_user_by_guid(self, guid: str) -> Optional[UserDTO]:
        user = self.user_repository.get_user_by_guid(guid)

        if not user:
            return None

        return UserDTO(guid=user.guid, nome=user.nome, email=user.email)