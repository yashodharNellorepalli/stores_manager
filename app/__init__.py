# Import flask and template operators
import os
from flask import Flask

# Application Definition
app = Flask(__name__,
            instance_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../instance'),
            instance_relative_config=True)

# Initializing configuration
app.config.from_pyfile('env.cfg', silent=True)

from app.extensions import mongo, MONGO_URI
mongo.init_app(app, MONGO_URI)

# Import a module / component using its blueprint handler variable (catalog_module)
from app.stores.controllers import stores_module

# Register blueprint(s)
app.register_blueprint(stores_module)
