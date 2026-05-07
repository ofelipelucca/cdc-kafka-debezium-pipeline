from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.postgres import get_db

from app.models.post import Post
from app.models.user import User

router = APIRouter()


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
        "created_at": post.created_at,
    }
