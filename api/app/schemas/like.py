from pydantic import BaseModel


class LikeDTO(BaseModel):
    guid: str
    id_user: int
    id_post: int
    user_guid: str
    post_guid: str

class LikeCreate(BaseModel):
    user_guid: str
    post_guid: str