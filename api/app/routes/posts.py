from fastapi import APIRouter, Depends, Response, status, HTTPException

from app.config import API_VERSION
from app.services.post_service import PostService
from app.services.like_service import LikeService
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

    post_service = PostService(post_repository=PostRepository(db=db), user_repository=user_repository)

    try:
        post = post_service.create_post(post_create=payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the post")

    return PostResponse(guid=post.guid, content=post.content, user_guid=post.user_guid, created_at=post.created_at)

@router.get("/posts/{guid}")
def get_post(guid: str, db=Depends(get_db)):
    post_service = PostService(post_repository=PostRepository(db=db), user_repository=UserRepository(db=db))

    try:
        post = post_service.get_post_by_guid(guid)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the post")

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponse(guid=post.guid, content=post.content, user_guid=post.user_guid, created_at=post.created_at)

@router.post("/posts/{guid}/like")
def like_post(guid: str, payload: LikeCreate, db=Depends(get_db)):
    like_service = LikeService(
        like_repository=LikeRepository(db=db),
        user_repository=UserRepository(db=db),
        post_repository=PostRepository(db=db)
    )

    try:
        payload.post_guid = guid
        like_service.create_like(like_create=payload)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while liking the post")

    return Response(status_code=status.HTTP_201_CREATED)