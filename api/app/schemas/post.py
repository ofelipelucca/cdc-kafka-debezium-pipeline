from pydantic import BaseModel
from datetime import datetime


class PostCreate(BaseModel):
    user_guid: str
    content: str


class PostResponse(BaseModel):
    guid: str
    content: str
    user_guid: str
    created_at: datetime