from kafka import KafkaConsumer
from pymongo import MongoClient
import json

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["cdc_db"]
collection = db["feed_posts"]

consumer = KafkaConsumer(
    'dbserver1.api_social_media.posts',
    bootstrap_servers='localhost:29092',
    auto_offset_reset='earliest',
    group_id='mongo-consumer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🚀 Consumindo e inserindo no Mongo...")

for msg in consumer:
    payload = msg.value
    op = payload.get("op")
    after = payload.get("after")

    if not after:
        continue

    doc = {
        "_id": after["id"],
        "user_id": after["id_user"],
        "content": after["content"]
    }

    if op == "c" or op == "u":
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": doc},
            upsert=True
        )

    elif op == "d":
        collection.delete_one({"_id": payload["before"]["id"]})

    print(f"Processado: {op} - {doc['_id']}")