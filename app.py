import logging

from flask import Flask

from config import Config

__all__ = ['create_app']

logger = logging.getLogger(__package__)


def create_app():
    """Create a Flask app."""

    app = Flask("ReadingList")
    app.config.from_object(Config())

    configure_blueprints(app)

    return app


def configure_blueprints(app):
    """Configure blueprints"""
    from core.api import graphql_api
    # from geography.restful.routes import countries

    app.register_blueprint(graphql_api)
    # app.register_blueprint(countries)
