import logging
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from app.schemas.post import PostDTO
from app.models.post import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, new_post: PostDTO) -> PostDTO:
        post = Post(content=new_post.content, id_user=new_post.id_user, guid=new_post.guid)

        try:
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post
        except Exception as e:
            self.db.rollback()
            logging.exception(f"Error creating post: {e}")
            raise

    def get_post_by_guid(self, guid: str) -> Optional[PostDTO]:
        try:
            post = self.db.query(Post).options(joinedload(Post.user)).filter(Post.guid == guid).one()
            return post
        except NoResultFound:
            logging.warning(f"Post with guid {guid} not found")
            return None
        except MultipleResultsFound:
            logging.error(f"Multiple posts found with guid {guid}")
            raise Exception(f"Multiple posts found with guid {guid}")
        except Exception as e:
            logging.exception(f"Error retrieving post by guid: {e}")
            raise