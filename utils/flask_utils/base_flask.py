import logging
from typing import Tuple
from flask import Flask


class BaseFlask:

    ENDPOINTS = [
        ('/is_alive', 'get_is_alive', ['GET'])
    ]

    def __init__(self, app_name: str, logger: logging.Logger):
        self.app_name = app_name
        self._app = Flask(app_name)
        self.is_alive = True
        self.logger = logger

    def get_app(self):
        return self._app

    def load_from_config(self, config: object):
        self._app.config.from_object(config)

    def get_is_alive(self, *args, **kwargs) -> Tuple[str, int]:
        return ('alive', 200) if self.is_alive else ('dead', 500)

    def run(self, host: str = "0.0.0.0", port: int = 5001, **kwargs):
        self._app.run(host, port, **kwargs)
