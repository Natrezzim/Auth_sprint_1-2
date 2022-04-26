import datetime
import os
from http import HTTPStatus

from flask import Blueprint
from flask_restful import Resource, reqparse, request

from src.app.db.db_models import Tokens, Users

from .datastore import UserDataStore

auth = Blueprint('auth', __name__)

EXPIRE_JWT = datetime.timedelta(days=14)
EXPIRE_ACCESS = datetime.timedelta(hours=2)
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
            # генерируем access и refresh токены
            access_token = UserDataStore.create_jwt_token(user_id=new_user_id, username=body["username"],
                                                          password=body["password"],
                                                          secret_key=new_user_id, expires_delta=EXPIRE_JWT)
            refresh_token = UserDataStore.create_jwt_token(user_id=new_user_id, username=body["username"],
                                                           password=body["password"],
                                                           secret_key=new_user_id, expires_delta=EXPIRE_ACCESS)
            # заливаем refresh токен в БД
            UserDataStore.save_refresh_token(refresh_token=refresh_token, user_id=new_user_id)
            return {"token": str(access_token), "refresh_token": str(refresh_token),
                    "message": "Create new user success"}, HTTPStatus.OK


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
            username=body["username"], password=body["password"], user_id=user_id, expires_delta=EXPIRE_JWT,
            secret_key=SECRET_KEY)
        refresh_token = UserDataStore.create_refresh_token(
            username=body["username"], password=body["password"], user_id=user_id, expires_delta=EXPIRE_ACCESS,
            secret_key=SECRET_KEY)
        # заливаем refresh токен в БД
        """"""
        return {"token": access_token, "refresh_token": refresh_token, "message": "Login success"}, HTTPStatus.OK


class RefreshAPI(Resource):

    @staticmethod
    def post(access_token: str, refresh_token: str):
        # Проверка Наличия refresh токена в БД
        refresh = Tokens.query.filter_by(refresh_token=refresh_token).one_or_none()
        if refresh is None:
            return {"message": "Refresh token not valid"}, HTTPStatus.UNAUTHORIZED
        # Проверка "свежести" refresh токена
        refresh_data = UserDataStore.get_user_data_from_token(token=refresh_token, secret_key=SECRET_KEY)
        current_time = datetime.datetime.now()
        refresh_expire_time = datetime.datetime.strptime(refresh_data["expires"], "%Y-%m-%dT%H:%M:%S")
        if current_time > refresh_expire_time:
            UserDataStore.delete_refresh_token(refresh_token)
            return {"message": "refresh_token expired"}, HTTPStatus.UNAUTHORIZED
        # проверка access токена
        access_data = UserDataStore.get_user_data_from_token(token=refresh_token, secret_key=SECRET_KEY)
        user = Users.query.filter_by(id=access_data["user_id"]).one_or_none()
        if user is None:
            return {"message": "Access token not valid"}, HTTPStatus.UNAUTHORIZED
        # генерация новго access токена
        new_access_token = UserDataStore.create_jwt_token(
            username=access_data["username"], password=access_data["password"], user_id=access_data["user_id"],
            expires_delta=EXPIRE_JWT, secret_key=SECRET_KEY)
        return {"token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK




        # class RefreshAPI(Resource):
#
#     def post(self, access_token: str, refresh_token: str):
#         try:
#             # Проверка валидности access / refresh токена
#             access_data = UserDataStore.get_user_data_from_token(token=access_token, secret_key=SECRET_KEY)
#             refresh_data = UserDataStore.get_user_data_from_token(token=refresh_token, secret_key=SECRET_KEY)
#             access_user = Users.query.filter_by(id=access_data['id']).one_or_none()
#             refresh_user = Users.query.filter_by(id=refresh_data['id']).one_or_none()
#             if access_user is None or refresh_user is None:
#                 return {"error": {"message": "Invalid access token or refresh token"}}, HTTPStatus.CONFLICT
#             # Проверка "свежести" refresh токена
#             current_time = datetime.datetime.now()
#             refresh_expire_time = datetime.datetime.strptime(refresh_user["expires"], "%Y-%m-%dT%H:%M:%S")
#             if current_time > refresh_expire_time:
#                 # удалить refresh токен из БД
#                 """"""
#                 return redirect('/api/v1/login', code=303)
#             # Проверка свежести
#
#             # получаем access токен из редис
#             exp_access_token = '' # redis.get(user_data[user_id])
#             if exp_access_token is None:
#                 new_access_token = UserDataStore.create_jwt_token(
#                     username=user_data["username"], password=user_data["password"], user_id=user_data["user_id"],
#                     expires_delta=EXPIRE_JWT, secret_key=SECRET_KEY)
#             try:
#                 assert access_token == exp_access_token
#             except AssertionError:
#                 return {"error": {"message": }}
