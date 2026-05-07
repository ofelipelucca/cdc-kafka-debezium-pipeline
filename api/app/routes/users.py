from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.models.user import User
from app.schemas.user import UserCreate

import uuid

router = APIRouter()


@router.post("/users")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(nome=payload.nome, email=payload.email, guid=str(uuid.uuid4()))

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"guid": user.guid}
