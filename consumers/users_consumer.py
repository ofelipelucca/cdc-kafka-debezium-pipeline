from base.base_consumer import BaseConsumer


class UsersConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(
            topic="dbserver1.api_social_media.users",
            collection_name="users",
            group_id="users-consumer"
        )

    def transform(self, after):
        return {
            "_id": after["id"],
            "nome": after["nome"],
            "email": after["email"],
            "guid": after["guid"]
        }


if __name__ == "__main__":
    consumer = UsersConsumer()
    consumer.run()
