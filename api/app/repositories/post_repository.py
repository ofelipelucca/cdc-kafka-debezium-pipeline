import logging
import Optional
from sqlalchemy.orm import Session

from app.models.post import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, content: str, id_user: int, guid: str) -> Post:
        post = Post(content=content, id_user=id_user, guid=guid)

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
        except Exception as e:
            logging.exception(f"Error retrieving post by guid: {e}")
            raise