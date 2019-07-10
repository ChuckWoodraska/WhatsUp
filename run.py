from app.app_factory import create_app
import os

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/config.ini")
app = create_app(config_path)
