import logging
import configurations
from torrent_downloader import TorrentDownloader
from utils.flask_utils.flask_utilities import FlaskUtilities
from utils.flask_utils.base_flask import BaseFlask
from utils.ext import LOGGER
from api.torrents.torrents_blueprint import torrents_bp
from api.torrents.torrents_view_blueprint import torrents_view_bp






class VODApi(BaseFlask):

    def __init__(self, name: str, logger: logging.Logger, config: str):
        super(VODApi, self).__init__(name, logger)
        self.load_from_config(config)


        FlaskUtilities.register_blueprint_to_app(self._app, torrents_bp)
        FlaskUtilities.register_blueprint_to_app(self._app, torrents_view_bp)


def main():
    app = VODApi("VOD API", LOGGER, "configurations.DevConfig")
    app.run("0.0.0.0", port=5001, debug=True)


if __name__ == '__main__':
    main()
