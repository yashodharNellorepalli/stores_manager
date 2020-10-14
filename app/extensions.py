from flask_pymongo import PyMongo

from .utils.general import get_config_value

mongo = PyMongo()
MONGO_URI = get_config_value("MONGO_URI")
