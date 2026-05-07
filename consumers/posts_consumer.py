from base.base_consumer import BaseConsumer

from pymongo import MongoClient


class PostsConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(
            topic="dbserver1.api_social_media.posts",
            collection_name="feed_posts",
            group_id="posts-consumer"
        )

        mongo_client = MongoClient("mongodb://localhost:27017/")
        db = mongo_client["cdc_db"]

        self.users_collection = db["users"]

    def transform(self, after):
        user = self.users_collection.find_one({"_id": after["id_user"]})

        return {
            "_id": after["id"],
            "guid": after["guid"],
            "content": after["content"],
            "user": {
                "id": user["_id"] if user else None,
                "guid": user["guid"] if user else None,
                "nome": user["nome"] if user else "Unknown",
            }
        }


if __name__ == "__main__":
    consumer = PostsConsumer()
    consumer.run()
