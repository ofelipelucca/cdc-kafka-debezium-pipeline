import uuid
from typing import Optional

from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostDTO


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def create_post(self, post_create: PostCreate) -> PostDTO:
        post_dto = PostDTO(guid=str(uuid.uuid4()), content=post_create.content, user_guid=post_create.user_guid, created_at=None)

        return self.post_repository.create_post(post_create=post_create | {"guid": post_dto.guid})

    def get_post_by_guid(self, guid: str) -> Optional[PostDTO]:
        post = self.post_repository.get_post_by_guid(guid)

        if not post:
            return None

        return PostDTO(guid=post.guid, content=post.content, user_guid=post.user.user_guid, created_at=post.created_at)