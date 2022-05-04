import os

from authlib.integrations.flask_client import OAuth
from flask import Flask

oauth = OAuth()

oauth.register(name='yandex')


def init_oauth(app: Flask):
    """

    :param app:
    """
    app.config["YANDEX_CLIENT_ID"] = os.getenv('YANDEX_CLIENT_ID')
    app.config["YANDEX_CLIENT_SECRET"] = os.getenv('YANDEX_CLIENT_SECRET')
    app.config["YANDEX_AUTHORIZE_URL"] = os.getenv('YANDEX_AUTHORIZE_URL')
    app.config["YANDEX_ACCESS_TOKEN_URL"] = os.getenv('YANDEX_ACCESS_TOKEN_URL')
    oauth.init_app(app)
