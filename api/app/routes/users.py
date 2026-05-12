import uuid
from fastapi import APIRouter, Depends, HTTPException

from app.config import API_VERSION
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.db.postgres import get_db


router = APIRouter(prefix=f"/api/{API_VERSION}")


@router.post("/users")
def create_user(payload: UserCreate, db=Depends(get_db)):
    user_repository = UserRepository(db=db)

    try:
        user = user_repository.create_user(user_create=payload | {"guid": str(uuid.uuid4())})
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the user") 

    return UserResponse(guid=user.guid, nome=user.nome, email=user.email)


@router.get("/users/{guid}")
def get_user(guid: str, db=Depends(get_db)):
    user_repository = UserRepository(db=db)

    try:
        user = user_repository.get_user_by_guid(guid)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the user")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(guid=user.guid, nome=user.nome, email=user.email)
