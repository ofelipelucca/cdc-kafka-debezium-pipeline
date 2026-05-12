import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.app.schemas.like import LikeCreate
from api.app.models.like import Like


class LikeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_like(self, like_create: LikeCreate) -> Like:
        like = Like(id_post=like_create.id_post, id_user=like_create.id_user, guid=like_create.guid)

        try:
            self.db.add(like)
            self.db.commit()
            self.db.refresh(like)
            return like
        except IntegrityError as e:
            self.db.rollback()
            logging.error(f"Integrity error creating like: {e}")
            raise
        except Exception as e:
            self.db.rollback()
            logging.exception(f"Error creating like: {e}")
            raise