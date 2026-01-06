from db.user import get_user_collection
from pprint import pprint

users_collection = get_user_collection()

users_collection.delete_many({})
