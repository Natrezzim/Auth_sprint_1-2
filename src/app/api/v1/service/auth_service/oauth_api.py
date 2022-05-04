from flask import Blueprint, redirect, url_for
from flask_restx import Resource

from src.app.oauth.oauth import oauth

auth = Blueprint('oauth', __name__)


class LoginYandex(Resource):
    @staticmethod
    def get():
        """

        :return: redirect to AuthorizationYandex class
        """
        redirect_url = url_for("authorization_yandex", _external=True)
        return oauth.yandex.authorize_redirect(redirect_url)


class AuthorizationYandex(Resource):
    @staticmethod
    def get():
        """

        :return: redirect to
        """
        token = oauth.yandex.authorize_access_token()
        response = oauth.yandex.get('https://login.yandex.ru/info')
        response.raise_for_status()
        profile = response.json()
        return redirect('/')

