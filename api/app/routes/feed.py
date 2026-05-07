from fastapi import APIRouter

from app.config import API_VERSION
from app.db.mongo import mongo_db

router = APIRouter(prefix=f"/api/{API_VERSION}")


@router.get("/feed")
def get_feed(n: int = 10):

    n = min(max(n, 1), 50)

    posts = list(mongo_db["feed_posts"].find({}, {"_id": 0}).sort("_id", -1).limit(n))

    return posts
