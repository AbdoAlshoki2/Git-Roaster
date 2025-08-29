
from typer import get_app_dir
import os

APP_NAME = "GitRoaster"
def get_config_path():
    config_dir = get_app_dir(APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")