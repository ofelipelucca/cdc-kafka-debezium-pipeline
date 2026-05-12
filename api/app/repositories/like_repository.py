import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.like import LikeDTO
from app.models.like import Like


class LikeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_like(self, new_like: LikeDTO) -> Like:
        like = Like(id_post=new_like.post_guid, id_user=new_like.user_guid, guid=new_like.guid)

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