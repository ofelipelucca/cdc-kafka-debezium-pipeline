import uuid

from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from app.repositories.like_repository import LikeRepository
from app.schemas.like import LikeCreate, LikeDTO


class LikeService:
    def __init__(self, like_repository: LikeRepository, user_repository: UserRepository, post_repository: PostRepository):
        self.like_repository = like_repository
        self.user_repository = user_repository
        self.post_repository = post_repository

    def create_like(self, like_create: LikeCreate) -> LikeDTO:
        user = self.user_repository.get_user_by_guid(like_create.user_guid)

        if not user:
            raise ValueError("User not found")

        post = self.post_repository.get_post_by_guid(like_create.post_guid)

        if not post:
            raise ValueError("Post not found")

        like_dto = LikeDTO(
            guid=str(uuid.uuid4()),
            id_user=user.id,
            id_post=post.id,
            user_guid=like_create.user_guid,
            post_guid=like_create.post_guid
        )

        return self.like_repository.create_like(new_like=like_dto)