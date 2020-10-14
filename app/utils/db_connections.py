from app import mongo


def get_mongo_db_connection():
    return mongo


def get_stores_master_collection():
    return mongo.db
