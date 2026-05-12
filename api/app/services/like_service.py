import uuid

from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from app.repositories.like_repository import LikeRepository
from app.schemas.like import LikeCreate, LikeDTO


class LikeService:
    def __init__(self, db):
        self.like_repository = LikeRepository(db=db)
        self.user_repository = UserRepository(db=db)
        self.post_repository = PostRepository(db=db)

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