import logging
import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from api.app.schemas.post import PostCreate
from app.models.post import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post_create: PostCreate) -> Post:
        post = Post(content=post_create.content, id_user=post_create.id_user, guid=post_create.guid)

        try:
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post
        except Exception as e:
            self.db.rollback()
            logging.exception(f"Error creating post: {e}")
            raise

    def get_post_by_guid(self, guid: str) -> Optional[Post]:
        try:
            post = self.db.query(Post).filter(Post.guid == guid).first()
            return post
        except NoResultFound:
            logging.warning(f"Post with guid {guid} not found")
            return None
        except Exception as e:
            logging.exception(f"Error retrieving post by guid: {e}")
            raise