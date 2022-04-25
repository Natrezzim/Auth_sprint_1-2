import datetime
import os
from http import HTTPStatus

from flask import Blueprint
from flask_restful import Resource, reqparse, request

from src.app.db.db_models import Tokens, Users

from .datastore import UserDataStore

auth = Blueprint('auth', __name__)


EXPIRE_REFRESH = datetime.timedelta(days=int(os.getenv('REFRESH_TOKEN_EXPIRED')))
EXPIRE_ACCESS = datetime.timedelta(hours=int(os.getenv('ACCESS_TOKEN_EXPIRED')))
SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class RegistrationAPI(Resource):
    """
    логика работы метода для регистрации нового пользователя api/auth/registration
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username")
    parser.add_argument('email', type=str, required=True, help="email")
    parser.add_argument('password', type=str, required=True, help="password")

    @staticmethod
    def post():
        body = request.get_json()
        # проверяем, что такого пользователя нет в БД
        check_user = Users.query.filter_by(username=body['username']).one_or_none()
        if check_user is not None:
            return {"error": {
                "message": "User with this username already exists"
            }}, HTTPStatus.CONFLICT
        else:
            new_user_id = UserDataStore.register_user(username=body["username"],
                                                      password=body["password"],
                                                      email=body["email"])
            return {"message": "Create new user success"}, HTTPStatus.OK


class LoginApi(Resource):
    """
    логика работы метода api/auth/login
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username")
    parser.add_argument('password', type=str, required=True, help="password")

    @staticmethod
    def post():
        body = request.get_json()
        # проверяем авторизационные данные
        user_id = UserDataStore.authorize_user(username=body.get('username'), password=body.get('password'),
                                               user_agent=request.headers.get('User-Agent'))
        if user_id is None:
            return {"error": {
                "message": "Email or password invalid"}}, HTTPStatus.UNAUTHORIZED
        # генерируем access и refresh токены
        access_token = UserDataStore.create_jwt_token(
            username=body["username"], password=body["password"], user_id=user_id, expires_delta=EXPIRE_ACCESS,
            secret_key=SECRET_KEY)
        refresh_token = UserDataStore.create_refresh_token(
            username=body["username"], password=body["password"], user_id=user_id, expires_delta=EXPIRE_REFRESH,
            secret_key=SECRET_KEY)
        # Проверяем наличие refresh токена в БД
        current_refresh = UserDataStore.get_refresh_token(user_id=user_id)
        if current_refresh:
            return {"message": "User is authorized"}
        # заливаем refresh токен в БД
        UserDataStore.save_refresh_token(refresh_token=refresh_token, user_id=user_id)
        return {"access_token": access_token, "refresh_token": refresh_token, "message": "Login success"}, HTTPStatus.OK


class RefreshAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('access_token', type=str, required=True, help="access_token")
    parser.add_argument('refresh_token', type=str, required=True, help="refresh_token")

    @staticmethod
    def post():
        body = request.get_json()
        # Проверка Наличия refresh токена в БД
        refresh = Tokens.query.filter_by(refresh_token=body['refresh_token']).one_or_none()
        if refresh is None:
            return {"message": "Refresh token not valid"}, HTTPStatus.UNAUTHORIZED
        # Проверка "свежести" refresh токена
        refresh_data = UserDataStore.get_user_data_from_token(token=body['refresh_token'], secret_key=SECRET_KEY)
        current_time = datetime.datetime.now()
        refresh_expire_time = datetime.datetime.strptime(refresh_data["expires"], "%Y-%m-%dT%H:%M:%S")
        if current_time > refresh_expire_time:
            UserDataStore.delete_refresh_token(body['refresh_token'])
            return {"message": "refresh_token expired"}, HTTPStatus.UNAUTHORIZED
        # проверка access токена
        access_data = UserDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
        user = Users.query.filter_by(id=access_data["user_id"]).one_or_none()
        if user is None:
            return {"message": "Access token not valid"}, HTTPStatus.UNAUTHORIZED
        # генерация новго access токена
        new_access_token = UserDataStore.create_jwt_token(
            username=access_data["username"], password=access_data["password"], user_id=access_data["user_id"],
            expires_delta=EXPIRE_ACCESS, secret_key=SECRET_KEY)
        return {"token": new_access_token, "refresh_token": body['refresh_token']}, HTTPStatus.OK


class LogoutAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('refresh_token', type=str, required=True, help="refresh_token")

    def post(self):
        body = request.get_json()
        refresh = Tokens.query.filter_by(refresh_token=body['refresh_token']).one_or_none()
        if refresh is None:
            return {"message": "Refresh token not valid"}, HTTPStatus.UNAUTHORIZED
        UserDataStore.delete_refresh_token(refresh.refresh_token)
        return HTTPStatus.NO_CONTENT


class HistoryAuthAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('access_token', type=str, required=True, help="access_token")

    def post(self):
        body = request.get_json()
        access_data = UserDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
        history_auth = UserDataStore.get_user_history_auth(user_id=access_data['user_id'])
        return {"history": str(history_auth)}


class ChangeAuthDataAPI(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('new_username', type=str, help="login")
    parser.add_argument('new_password', type=str, help="password")
    parser.add_argument('access_token', type=str, required=True, help="access_token")

    def post(self):
        body = request.get_json()
        access_data = UserDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
        if body.get("new_username", None) is not None:
            UserDataStore.change_login_user(user_id=access_data["user_id"], new_username=body["new_username"])
        if body.get("new_password", None) is not None:
            UserDataStore.change_password_user(user_id=access_data["user_id"], new_password=body["new_password"])
        else:
            return {"messaage": "Expected Login or Password for changed"}, HTTPStatus.BAD_REQUEST

        return HTTPStatus.NO_CONTENT
