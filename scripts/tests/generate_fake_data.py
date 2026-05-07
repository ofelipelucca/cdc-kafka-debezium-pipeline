from faker import Faker

import requests
import random
import logging

from concurrent.futures import ThreadPoolExecutor, as_completed


logging.basicConfig(level=logging.INFO)

fake = Faker("pt_BR")

API_URL = "http://localhost:8000/api/v1"
TOTAL_USERS = 100
TOTAL_POSTS = 10_000
MAX_WORKERS = 50

user_guids = []


def create_user(index: int):
    payload = {"nome": fake.name(), "email": fake.unique.email()}
    response = requests.post(f"{API_URL}/users", json=payload, timeout=10)

    response.raise_for_status()

    data = response.json()

    logging.info(f"[{index + 1}/{TOTAL_USERS}] User {data['guid']} created")

    return data["guid"]


def create_post(index: int):
    payload = {
        "user_guid": random.choice(user_guids),
        "content": fake.text(max_nb_chars=300),
    }

    response = requests.post(f"{API_URL}/posts", json=payload, timeout=10)
    response.raise_for_status()

    if index != 0 and index % 100 == 0:
        logging.info(f"[{index}/{TOTAL_POSTS}] {index} posts created")


logging.info("Creating users...")


with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(create_user, i) for i in range(TOTAL_USERS)]

    for future in as_completed(futures):
        try:
            guid = future.result()
            user_guids.append(guid)
        except Exception as e:
            logging.exception(f"Error creating user: {e}")


logging.info(f"{len(user_guids)} users created")

logging.info("Creating posts...")


with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(create_post, i) for i in range(TOTAL_POSTS)]

    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            logging.exception(f"Error creating post: {e}")


logging.info("Finished")
