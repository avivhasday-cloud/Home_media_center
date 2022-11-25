from api.torrents.torrents_blueprint import TorrentsBlueprint
from utils.flask_utils.flask_utilities import FlaskUtilities
from flask import render_template
from flask.blueprints import Blueprint
from configurations import STATIC_DIR, TEMPLATES_DIR


class TorrentsViewBlueprint(Blueprint):

    ENDPOINTS = [
        ('/browse', 'browse_view', ['GET']),
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
        super(TorrentsViewBlueprint, self).__init__(name, import_name, static_folder=static_folder, template_folder=template_folder, url_prefix=url_prefix)
        FlaskUtilities.init_endpoints(self, TorrentsViewBlueprint.ENDPOINTS)

    @staticmethod
    def browse_view(**kwargs):
        res, status_code = TorrentsBlueprint.browse(**kwargs)
        return render_template('browse_view.html', title='Browse Torrents', **res), status_code

    @staticmethod
    def download(**kwargs):
        text, status_code = TorrentsBlueprint.download(**kwargs)
        return render_template('general_message.html', title='Homepage', message=text), status_code

    @staticmethod
    def pause(**kwargs):
        text, status_code = TorrentsBlueprint.pause(**kwargs)
        res, _ = TorrentsBlueprint.get_details(**kwargs)
        return render_template('torrent_client_view.html', title='Torrent Client', **res), status_code

    @staticmethod
    def resume(**kwargs):
        text, status_code = TorrentsBlueprint.resume(**kwargs)
        res, _ = TorrentsBlueprint.get_details(**kwargs)
        return render_template('torrent_client_view.html', title='Torrent Client', **res), status_code

    @staticmethod
    def get_details(**kwargs):
        res, status_code = TorrentsBlueprint.get_details(**kwargs)
        return render_template('torrent_client_view.html', title='Torrent Client', **res), status_code

    @staticmethod
    def remove(**kwargs):
        text, status_code = TorrentsBlueprint.remove(**kwargs)
        return render_template('general_message.html', title='Homepage', message=text), status_code


torrents_view_bp = TorrentsViewBlueprint("torrents_view_bp", __name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR, url_prefix='/views/torrents')
