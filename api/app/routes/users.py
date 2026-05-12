from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import API_VERSION
from app.db.postgres import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

import uuid

router = APIRouter(prefix=f"/api/{API_VERSION}")


@router.post("/users")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(nome=payload.nome, email=payload.email, guid=str(uuid.uuid4()))

    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(guid=user.guid, nome=user.nome, email=user.email)


@router.get("/users/{guid}")
def get_user(guid: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.guid == guid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(guid=user.guid, nome=user.nome, email=user.email)
