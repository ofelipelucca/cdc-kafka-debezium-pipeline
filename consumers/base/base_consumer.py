from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import logging

logging.basicConfig(level=logging.INFO)


class BaseConsumer:
    def __init__(self, topic, collection_name, group_id="mongo-consumer"):
        self.topic = topic

        mongo_client = MongoClient("mongodb://localhost:27017/")
        db = mongo_client["cdc_db"]

        self.collection = db[collection_name]

        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers="localhost:29092",
            auto_offset_reset="earliest",
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")) if x else None
        )

    def transform(self, after):
        raise NotImplementedError

    def run(self):
        logging.info(f"Consumer started for topic: {self.topic}")

        for msg in self.consumer:
            if not msg.value:
                logging.warning("Received empty message, skipping")
                continue
            
            payload = msg.value.get("payload")
            
            if not payload:
                logging.warning("Received empty payload, skipping")
                continue

            op = payload.get("op")
            after = payload.get("after")
            before = payload.get("before")

            try:
                if op in ["c", "u"]:
                    doc = self.transform(after)
                    self.collection.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
                    action = "created" if op == "c" else "updated"
                    logging.info(f"Document {action}: {doc['_id']} - {doc['guid']}")
                elif op == "d":
                    self.collection.delete_one({"_id": before["id"]})
                    logging.info(f"Document deleted: {before['id']} - {before['guid']}")

            except Exception as e:
                logging.exception(f"Error processing event: {e}")
