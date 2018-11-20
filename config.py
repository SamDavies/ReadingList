import os


class Config(object):
    # Get app root path, also can use flask.root_path.
    # ../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'sdfsdf82347$e%$%$%$&fsdfs!!ASx+__WEBB$'
