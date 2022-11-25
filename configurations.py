import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    TORRENT_CLIENT_IP = os.getenv('TORRENT_CLIENT_IP')
    PORT = os.getenv('PORT')
    SERVER_URL = f'http://{TORRENT_CLIENT_IP}:{PORT}/'
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    OUTPUT_PATH = os.getenv('OUTPUT_PATH')


class ServerConfig:
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_PATH = os.getenv('UPLOAD_PATH')
