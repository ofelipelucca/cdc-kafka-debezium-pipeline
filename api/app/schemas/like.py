from pydantic import BaseModel


class LikeCreate(BaseModel):
    user_guid: str
    post_guid: str