import logging
import configurations
from managers.general_manager import GeneralManager
from utils.flask_utils.flask_utilities import FlaskUtilities
from utils.flask_utils.base_flask import BaseFlask
from utils.ext import LOGGER
from api.torrents.torrents_blueprint import TorrentsBlueprint
from api.torrents.torrents_view_blueprint import TorrentsViewBlueprint


class VODApi(BaseFlask):

    def __init__(self, name: str, torrents_downloader_creds: [str], logger: logging.Logger, config: str):
        super(VODApi, self).__init__(name, logger)
        self.load_from_config(config)
        self.general_manager = GeneralManager(torrents_downloader_creds ,self.logger)
        self.torrents_bp = TorrentsBlueprint("torrents_bp", TorrentsBlueprint.__module__, static_folder=configurations.STATIC_DIR, template_folder=configurations.TEMPLATES_DIR, url_prefix='/api/torrents/', manager=self.general_manager)
        self.torrents_view_bp = TorrentsViewBlueprint("torrents_view_bp", TorrentsViewBlueprint.__module__, static_folder=configurations.STATIC_DIR, template_folder=configurations.TEMPLATES_DIR, url_prefix='/views/torrents', manager=self.general_manager)

        # initializing endpoints to blueprints
        FlaskUtilities.init_endpoints(self.torrents_bp, TorrentsBlueprint.ENDPOINTS)
        FlaskUtilities.init_endpoints(self.torrents_view_bp, TorrentsViewBlueprint.ENDPOINTS)

        # register blueprints to app
        FlaskUtilities.register_blueprint_to_app(self._app, self.torrents_bp)
        FlaskUtilities.register_blueprint_to_app(self._app, self.torrents_view_bp)

    def run(self, host: str = "0.0.0.0", port: int = 5001, **kwargs):
        self.general_manager.run()
        super(VODApi, self).run(host, port, **kwargs)


def main():
    torrents_downloader_creds = [configurations.BaseConfig.SERVER_URL, configurations.BaseConfig.USER,
                                       configurations.BaseConfig.PASSWORD, configurations.BaseConfig.TORRENTS_RELATIVE_OUTPUT_PATH]
    app = VODApi("VOD API", torrents_downloader_creds, LOGGER, "configurations.DevConfig")
    app.run("0.0.0.0", port=5001, debug=False)


if __name__ == '__main__':
    main()
