from faker import Faker

import requests
import random
import logging

logging.basicConfig(level=logging.INFO)

fake = Faker("pt_BR")

API_URL = "http://localhost:8000/api/v1"
TOTAL_USERS = 100
TOTAL_POSTS = 10_000

user_guids = []

logging.info("Creating users...")

for _ in range(TOTAL_USERS):
    payload = {"nome": fake.name(), "email": fake.unique.email()}

    response = requests.post(f"{API_URL}/users", json=payload)

    data = response.json()

    user_guids.append(data["guid"])
    
    logging.info(f"[{len(user_guids)}/{TOTAL_USERS}] User {data['guid']} created")

logging.info(f"{len(user_guids)} users created")

logging.info("Creating posts...")

for i in range(TOTAL_POSTS):
    payload = {
        "user_guid": random.choice(user_guids),
        "content": fake.text(max_nb_chars=300),
    }

    requests.post(f"{API_URL}/posts", json=payload)

    if i % 100 == 0:
        logging.info(f"{i} posts created")


logging.info("Finished")
