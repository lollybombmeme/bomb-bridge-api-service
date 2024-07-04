# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from .logger import Logger

import sentry_sdk
from celery import Celery

from flask import Flask

from sentry_sdk.api import capture_message
from sentry_sdk.integrations.flask import FlaskIntegration


def create_app(config=None, app_name=None):
    """Create a Flask app."""
    if app_name is None:
        app_name = config.PROJECT

    app = Flask(app_name, instance_relative_config=True)
    configure_app(app, config)
    configure_extensions(app)

    return app


def configure_app(app, config):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)


def configure_extensions(app):
    if app.config.get('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[FlaskIntegration()],
            debug=True,
            server_name=app.config.get('PROJECT')
        )

        capture_message('{} celery starts'.format(app.config.get('PROJECT')))


def create_worker(app_config):
    app = create_app(app_config)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    Logger.debug('Init Celery tasks app')

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
