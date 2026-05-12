import uuid
from typing import Optional

from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.post import PostCreate, PostDTO


class PostService:
    def __init__(self, post_repository: PostRepository, user_repository: UserRepository):
        self.post_repository = post_repository
        self.user_repository = user_repository

    def create_post(self, post_create: PostCreate) -> PostDTO:
        user = self.user_repository.get_user_by_guid(post_create.user_guid)

        if not user:
            raise ValueError("User not found")

        post_dto = PostDTO(guid=str(uuid.uuid4()), content=post_create.content, id_user=user.id, user_guid=user.guid, created_at=None)


        return self.post_repository.create_post(new_post=post_dto)

    def get_post_by_guid(self, guid: str) -> Optional[PostDTO]:
        post = self.post_repository.get_post_by_guid(guid)

        if not post:
            return None

        return PostDTO(guid=post.guid, content=post.content, user_guid=post.user.user_guid, created_at=post.created_at)