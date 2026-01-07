from db import Database
from configs import CONFIG as config
from pymongo.collection import Collection


def get_user_collection() -> Collection:
    client = Database().client

    db = client[config.DB_NAME]
    users_collection = db['users']
    return users_collection
