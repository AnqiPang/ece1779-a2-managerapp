from .base import *


def init_app(app):
    db.init_app(app)
    db.create_all('__all__', app)
    return app
