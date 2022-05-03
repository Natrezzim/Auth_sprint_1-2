from flask import Blueprint, url_for, session, redirect
from flask_restx import Resource

from src.app.oauth.oauth import oauth

auth = Blueprint('oauth', __name__)

oauth.register(
    name='yandex',
    server_metadata_url='https://oauth.yandex.ru/',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


class AuthorizationYandex(Resource):
    @staticmethod
    def get():
        token = oauth.yandex.authorize_access_token()
        print(token)
        return redirect('/')
