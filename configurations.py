import os
from pathlib import Path
from dotenv import load_dotenv


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
STATIC_DIR = os.path.join(ROOT_DIR, 'static')


class BaseConfig:
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    TORRENT_CLIENT_IP = os.getenv('TORRENT_CLIENT_IP')
    PORT = os.getenv('PORT')
    SERVER_URL = f'http://{TORRENT_CLIENT_IP}:{PORT}/'
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    OUTPUT_PATH = os.getenv('OUTPUT_PATH')


class DevConfig(BaseConfig):
    DEBUG = True


class ServerConfig:
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_PATH = os.getenv('UPLOAD_PATH')
