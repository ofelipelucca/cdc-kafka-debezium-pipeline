from pydantic import BaseModel
from datetime import datetime


class PostResponse(BaseModel):
    guid: str
    content: str
    user_guid: str
    created_at: datetime
