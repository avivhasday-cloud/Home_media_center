from flask.blueprints import Blueprint

from managers.general_manager import GeneralManager
from utils.bs4_parser import BS4Parser
from utils.common import Fields
from utils.flask_utils.flask_utilities import FlaskUtilities
from utils.torrent_site_api import TorrentSiteAPI
from utils.ext import TORRENT_DOWNLOADER
from configurations import STATIC_DIR, TEMPLATES_DIR
from http import HTTPStatus


class TorrentsBlueprint(Blueprint):

    ENDPOINTS = [
        ('/browse', 'browse', ['GET']),
        ('/download', 'download', ['POST']),
        ('/resume', 'resume', ['PUT']),
        ('/pause', 'pause', ['PUT']),
        ('/', 'get_details', ['GET']),
        ('/', 'remove', ['DELETE']),
    ]

    def __init__(self,
                 name: str,
                 import_name: str,
                 manager: GeneralManager,
                 static_folder: str = None,
                 template_folder: str = None,
                 url_prefix: str = None,
                 ):
        super(TorrentsBlueprint, self).__init__(name, import_name, static_folder=static_folder, template_folder=template_folder, url_prefix=url_prefix)
        self.manager = manager

    @staticmethod
    def browse(**kwargs):
        headers = Fields.BROWSE_TORRENTS_HEADERS[1::]
        keyword_to_search = kwargs.get("search", None)
        if keyword_to_search:
            data = TorrentSiteAPI.get_search_query_content(keyword_to_search)
            status_code = HTTPStatus.OK if len(data) > 0 else HTTPStatus.NOT_FOUND
        else:
            data = None
            status_code = HTTPStatus.OK
        res = {"headers": headers, "data": data}
        return res, status_code

    def download(self, **kwargs):
        torrent_data = kwargs.get("torrent_details", None)
        status = self.manager.add_to_download_queue(torrent_data)
        return (f"{torrent_data['name']} added to queue", HTTPStatus.CREATED) if status \
            else (f"Failed to add to queue {torrent_data['name']}", HTTPStatus.INTERNAL_SERVER_ERROR)

    def resume(self, **kwargs):
        torrent_details = kwargs.get("torrent_details", None)
        status = self.manager.handle_torrent(torrent_details, "resume")
        return (f"{torrent_details['name']} has been resumed", HTTPStatus.OK) if status \
            else (f"Failed to resume downloading {torrent_details['name']}", HTTPStatus.INTERNAL_SERVER_ERROR)

    def pause(self, **kwargs):
        torrent_details = kwargs.get("torrent_details", None)
        status = self.manager.handle_torrent(torrent_details, "pause")
        return (f"{torrent_details['name']} has been paused", HTTPStatus.OK) if status \
            else (f"Failed to pause downloading {torrent_details['name']}", HTTPStatus.INTERNAL_SERVER_ERROR)

    def get_details(self, **kwargs):
        filter_keyword = kwargs.get("filter_keyword", None)
        torrent_details = self.manager.get_torrents_details(filter_keyword)
        headers = Fields.TORRENT_DETAILS_HEADERS
        status_code = HTTPStatus.OK if len(torrent_details) > 0 else HTTPStatus.NOT_FOUND
        res = {"headers": headers, "data": torrent_details}
        return res, status_code

    def remove(self, **kwargs):
        torrent_details = kwargs.get("torrent_details", None)
        status = self.manager.handle_torrent(torrent_details, "remove")
        return (f"{torrent_details['name']} has been removed", HTTPStatus.OK) if status \
            else (f"Failed to remove {torrent_details['name']}", HTTPStatus.INTERNAL_SERVER_ERROR)

