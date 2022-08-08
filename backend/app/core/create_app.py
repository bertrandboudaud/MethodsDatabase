from app.config import config
from app.extensions import api, init_app_extensions, webargs
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from marshmallow import ValidationError
from typing import Any

from .cli import register_cli_handlers
import flask_login
from flask_login import UserMixin

# from app.auth.authentication import basic_auth

class User(UserMixin):
    id = 42

def register_api(app: Flask) -> None:
    """Register blueprints and routes."""

    @app.route("/api")
    @cross_origin()
    def hello() -> Any:
        return jsonify({"message": "Hello"})

    @app.route('/api/login/<user>/<password>', methods=['GET', 'POST'])
    @cross_origin()
    def login(user, password):
        # Here we use a class of some kind to represent and validate our
        # client-side form data. For example, WTForms is a library that will
        # handle this for us, and we use a custom LoginForm to validate.
        #form = LoginForm()
        #if form.validate_on_submit():
        #if True:
        if user == "bertrand" and password =="toto":
            # Login and validate the user.
            # user should be an instance of your `User` class
            example_user = User() # TODO implement user db. here we have one unique user
            flask_login.login_user(example_user)

            # TODO next = flask.request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #    return flask.abort(400)

            return jsonify({'success':True}), 200, {'ContentType':'application/json'} 
        return jsonify({"errors": "Invalid user/password"}), 400, {'ContentType':'application/json'} 

    from app.forum.api import blueprint as forum_blueprint
    from app.user.api import blueprint as user_blueprint
    from app.instrument.api import blueprint as instrument_blueprint
    from app.compound.api import blueprint as compound_blueprint
    from app.eluent.api import blueprint as eluent_blueprint
    from app.column.api import blueprint as column_blueprint
    from app.method.api import blueprint as method_blueprint

    api.register_blueprint(user_blueprint)
    api.register_blueprint(instrument_blueprint)
    api.register_blueprint(compound_blueprint)
    api.register_blueprint(eluent_blueprint)
    api.register_blueprint(column_blueprint)
    api.register_blueprint(method_blueprint)
    api.register_blueprint(forum_blueprint)


def register_api_error_handlers(app: Flask) -> None:
    """Register error handlers for API.

    These are generic handlers that apply to all API requests.
    """

    @webargs.error_handler
    def handle_error(
        error, req, schema, error_status_code, error_headers
    ):  # type: ignore
        if "json" in error.messages:
            raise ValidationError(error.messages["json"])
        if "path" in error.messages:
            raise ValidationError(error.messages["path"])
        raise ValidationError(error.messages)

    @app.errorhandler(ValidationError)
    def validateion_error(error):  # type: ignore
        return jsonify({"errors": error.normalized_messages()}), 400


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.secret_key = 'super secret key'
    init_app_extensions(app)

    # Note: unsafe, better set origins to known hosts
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API methods.
    register_api(app)
    # Register error handlers.
    register_api_error_handlers(app)
    # Register cli commands.
    register_cli_handlers(app)
    # Init flask admin - disabled for now as it doesn't have
    # authentication, so we can't have it like this on develop/production
    # also, it is not usable for now
    # init_admin(app)
    return app
