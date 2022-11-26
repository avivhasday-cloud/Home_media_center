from flask.blueprints import Blueprint
from utils.bs4_parser import BS4Parser
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
                 static_folder: str = None,
                 template_folder: str = None,
                 url_prefix: str = None,
                 ):
        super(TorrentsBlueprint, self).__init__(name, import_name, static_folder=static_folder, template_folder=template_folder, url_prefix=url_prefix)
        FlaskUtilities.init_endpoints(self, TorrentsBlueprint.ENDPOINTS)

    @staticmethod
    def browse(**kwargs):
        headers = BS4Parser.TABLE_CELLS_KEYS[1::]
        keyword_to_search = kwargs.get("search", None)
        if keyword_to_search:
            data = TorrentSiteAPI.get_search_query_content(keyword_to_search)
            status_code = HTTPStatus.OK if len(data) > 0 else HTTPStatus.NOT_FOUND
        else:
            data = None
            status_code = HTTPStatus.OK
        res = {"headers": headers, "data": data}
        return res, status_code

    @staticmethod
    def download(**kwargs):
        torrent_data = kwargs.get("torrent_details", None)
        status = TORRENT_DOWNLOADER.add_to_download_torrent_queue(torrent_data)
        return (f"{torrent_data['name']} added to queue", HTTPStatus.CREATED) if status \
            else (f"Failed to add to queue {torrent_data['name']}", HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    def resume(**kwargs):
        torrent_details = kwargs.get("torrent_details", None)
        status = TORRENT_DOWNLOADER.resume_downloading_torrent(torrent_details)
        return (f"{torrent_details['name']} has been resumed", HTTPStatus.OK) if status \
            else (f"Failed to resume downloading {torrent_details['name']}", HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    def pause(**kwargs):
        torrent_details = kwargs.get("torrent_details", None)
        status = TORRENT_DOWNLOADER.pause_downloading_torrent(torrent_details)
        return (f"{torrent_details['name']} has been paused", HTTPStatus.OK) if status \
            else (f"Failed to pause downloading {torrent_details['name']}", HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_details(**kwargs):
        filter_keyword = kwargs.get("filter_keyword", None)
        torrent_details = TORRENT_DOWNLOADER.get_torrents_details(filter_keyword)
        headers = TORRENT_DOWNLOADER.TORRENT_DETAILS_KEYS
        status_code = HTTPStatus.OK if len(torrent_details) > 0 else HTTPStatus.NOT_FOUND
        res = {"headers": headers, "data": torrent_details}
        return res, status_code

    @staticmethod
    def remove(**kwargs):
        torrent_details = kwargs.get("torrent_details", None)
        status = TORRENT_DOWNLOADER.remove_torrent_and_its_contents(torrent_details)
        return (f"{torrent_details['name']} has been removed", HTTPStatus.OK) if status \
            else (f"Failed to remove {torrent_details['name']}", HTTPStatus.INTERNAL_SERVER_ERROR)


torrents_bp = TorrentsBlueprint("torrents_blueprint", __name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR, url_prefix='/api/torrents/')
