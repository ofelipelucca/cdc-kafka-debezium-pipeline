import uuid
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.exc import IntegrityError

from app.config import API_VERSION
from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from app.repositories.like_repository import LikeRepository
from app.schemas.post import PostCreate, PostResponse
from app.schemas.like import LikeCreate
from app.db.postgres import get_db


router = APIRouter(prefix=f"/api/{API_VERSION}")


@router.post("/posts")
def create_post(payload: PostCreate, db=Depends(get_db)):
    user_repository = UserRepository(db=db)

    user = user_repository.get_user_by_guid(payload.user_guid)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    post_repository = PostRepository(db=db)

    try:
        post = post_repository.create_post(post_create=payload | {"guid": str(uuid.uuid4())})
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the post")

    return PostResponse(guid=post.guid, content=post.content, user_guid=user.guid, created_at=post.created_at)


@router.get("/posts/{guid}")
def get_post(guid: str, db=Depends(get_db)):
    post_repository = PostRepository(db=db)

    try:
        post = post_repository.get_post_by_guid(guid)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the post")

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponse(guid=post.guid, content=post.content, user_guid=post.user.user_guid, created_at=post.created_at)



@router.post("/posts/{guid}/like")
def like_post(guid: str, payload: LikeCreate, db=Depends(get_db)):
    user_repository = UserRepository(db=db)

    user = user_repository.get_user_by_guid(payload.user_guid)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    post_repository = PostRepository(db=db)

    post = post_repository.get_post_by_guid(guid)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    like_repository = LikeRepository(db=db)

    try:
        like_repository.create_like(like_create=payload | {"guid": str(uuid.uuid4()), "id_post": post.id, "id_user": user.id})
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User has already liked this post")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while liking the post")

    return Response(status_code=status.HTTP_201_CREATED)