from app import app as current_app


def get_config_value(key):
    return current_app.config[key]
