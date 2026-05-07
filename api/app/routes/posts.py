from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.config import API_VERSION
from app.schemas.post import PostCreate
from app.db.postgres import get_db
from app.models.post import Post
from app.models.user import User

import uuid

router = APIRouter(prefix=f"/api/{API_VERSION}")


@router.post("/posts")
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.guid == payload.user_guid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    post = Post(content=payload.content, id_user=user.id, guid=str(uuid.uuid4()))

    db.add(post)
    db.commit()
    db.refresh(post)

    return {"guid": post.guid}


@router.get("/posts/{guid}")
def get_post(guid: str, db: Session = Depends(get_db)):
    result = (
        db.query(Post, User)
        .join(User, User.id == Post.id_user)
        .filter(Post.guid == guid)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    post, user = result

    return {
        "guid": post.guid,
        "content": post.content,
        "user_guid": user.guid,
        "created_at": post.created_at
    }
