import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.schemas.user import UserDTO
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, new_user: UserDTO) -> UserDTO:
        user = User(nome=new_user.nome, email=new_user.email, guid=new_user.guid)

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return UserDTO(guid=user.guid, nome=user.nome, email=user.email)
        except Exception as e:
            self.db.rollback()
            logging.exception(f"Error creating user: {e}")
            raise e

    def get_user_by_guid(self, guid: str) -> Optional[UserDTO]:
        try:
            user = self.db.query(User).filter(User.guid == guid).one()
            return UserDTO(guid=user.guid, nome=user.nome, email=user.email)
        except NoResultFound:
            logging.warning(f"User with guid {guid} not found")
            return None
        except MultipleResultsFound:
            logging.error(f"Multiple users found with guid {guid}")
            raise Exception(f"Multiple users found with guid {guid}")
        except Exception as e:
            logging.exception(f"Error retrieving user by guid: {e}")
            raise e