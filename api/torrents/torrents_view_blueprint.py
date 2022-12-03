from api.torrents.torrents_blueprint import TorrentsBlueprint
from managers.general_manager import GeneralManager
from utils.flask_utils.flask_utilities import FlaskUtilities
from flask import render_template
from flask.blueprints import Blueprint
from configurations import STATIC_DIR, TEMPLATES_DIR

BLUEPRINT_NAME = "torrents_view_bp"


class TorrentsViewBlueprint(TorrentsBlueprint):

    ENDPOINTS = [
        ('/browse', 'browse_view', ['GET']),
        ('/download', 'download_view', ['POST']),
        ('/resume', 'resume_view', ['PUT']),
        ('/pause', 'pause_view', ['PUT']),
        ('/', 'get_details_view', ['GET']),
        ('/', 'remove_view', ['DELETE']),

    ]

    #todo: find better names for functions or change the way rendering to html.
    def __init__(self,
                 name: str,
                 import_name: str,
                 manager: GeneralManager,
                 static_folder: str = None,
                 template_folder: str = None,
                 url_prefix: str = None,
                 ):
        super(TorrentsViewBlueprint, self).__init__(name, import_name, static_folder=static_folder, template_folder=template_folder, url_prefix=url_prefix, manager=manager)

    @staticmethod
    def browse_view(**kwargs):
        res, status_code = TorrentsBlueprint.browse(**kwargs)
        res.update({"bp": BLUEPRINT_NAME, "button_names_to_methods_map": [{"download_view": "POST"}]})
        return render_template('browse_view.html', title='Browse Torrents', **res), status_code

    def download_view(self, **kwargs):
        text, status_code = self.download(**kwargs)
        return render_template('general_message.html', title='Homepage', message=text), status_code

    def pause_view(self, **kwargs):
        text, status_code = self.pause(**kwargs)
        return self.get_details_view(**kwargs)

    def resume_view(self, **kwargs):
        text, status_code = self.resume(**kwargs)
        return self.get_details_view(**kwargs)

    def get_details_view(self, **kwargs):
        res, status_code = self.get_details(**kwargs)
        res.update({"bp": BLUEPRINT_NAME, "button_names_to_methods_map": [{"resume_view": "PUT"}, {"pause_view": "PUT"},
                                                                          {"remove_view": "DELETE"}]})
        return render_template('torrent_client_view.html', title='Torrent Client', **res), status_code

    def remove_view(self, **kwargs):
        text, status_code = self.remove(**kwargs)
        return render_template('general_message.html', title='Homepage', message=text), status_code

