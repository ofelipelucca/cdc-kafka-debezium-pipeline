import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.schemas.user import UserCreate
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate) -> User:
        user = User(nome=user_create.nome, email=user_create.email, guid=user_create.guid)

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            logging.exception(f"Error creating user: {e}")
            raise e

    def get_user_by_guid(self, guid: str) -> Optional[User]:
        try:
            user = self.db.query(User).filter(User.guid == guid).first()
            return user
        except NoResultFound:
            logging.warning(f"User with guid {guid} not found")
            return None
        except Exception as e:
            logging.exception(f"Error retrieving user by guid: {e}")
            raise e