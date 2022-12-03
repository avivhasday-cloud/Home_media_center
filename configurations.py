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
    USER = os.getenv("TORRENT_USER")
    PASSWORD = os.getenv("PASSWORD")
    TORRENTS_RELATIVE_OUTPUT_PATH = os.getenv('TORRENTS_RELATIVE_OUTPUT_PATH')
    TORRENTS_OUTPUT_PATH = os.getenv("TORRENTS_OUTPUT_PATH")
    TORRENTS_ABS_OUTPUT_PATH = os.path.join(TORRENTS_OUTPUT_PATH, TORRENTS_RELATIVE_OUTPUT_PATH)


class DevConfig(BaseConfig):
    DEBUG = True


class ServerConfig:
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_PATH = os.getenv('UPLOAD_PATH')
