from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_smorest import Api
from flask_smorest.arguments import ArgumentsMixin

from flask_login import LoginManager
from flask_login import UserMixin

db = SQLAlchemy()
migrate = Migrate()
webargs = ArgumentsMixin.ARGUMENTS_PARSER
api = Api()
login_manager = LoginManager()


def init_app_extensions(app: Flask):
    """Initialize the extensions with app instance."""
    db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

example_user = UserMixin() # TODO implement user db. here we have one unique user

@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id) # TODO implement user db. here we have one unique user
    return example_user
