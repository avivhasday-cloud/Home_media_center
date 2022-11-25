from flask import request, Flask, make_response, jsonify
from flask.blueprints import Blueprint
from typing import Callable, List, Union


class EndpointAction(object):

    "Class for handling server function and return response object"

    def __init__(self, action: Callable):
        self.action = action

    def __call__(self, **kwargs):
        kwargs.update(request.args)
        kwargs.update(request.form)
        if request.is_json and request.json:
            kwargs.update(request.json)
        if request.files:
            kwargs['files'] = request.files
        res, status_code = self.action(**kwargs)
        if isinstance(res, str):
            res_object = make_response(res, status_code)
        else:
            res_object = make_response(jsonify(res), status_code)
        return res_object


class FlaskUtilities:

    @staticmethod
    def add_endpoint(app: Union[Flask, Blueprint], endpoint: str = None, handler_name: str = None, methods=List[str]):
        app.add_url_rule(endpoint, endpoint=handler_name, view_func=EndpointAction(getattr(app, handler_name)), methods=methods)

    @staticmethod
    def register_blueprint_to_app(app: Flask, blueprint: any):
        app.register_blueprint(blueprint)

    @staticmethod
    def init_endpoints(app: Union[Flask, Blueprint], endpoints: List[tuple]):
        for endpoint in endpoints:
            FlaskUtilities.add_endpoint(app, *endpoint)
