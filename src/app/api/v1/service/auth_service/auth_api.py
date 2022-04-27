import datetime
import os
from http import HTTPStatus

from flask import Blueprint, request, jsonify
from flask_restx import reqparse, Resource

from src.app.api.v1.service.datastore.roles_datastore import RolesCRUD
from src.app.db.db_models import Tokens, Users, UserRole
from src.app.api.v1.service.datastore.token_datastore import TokenDataStore

from src.app.api.v1.service.datastore.user_datastore import UserDataStore
from src.app.api.v1.service.check_user import CheckAuthUser
from src.app.utils.pagination import get_paginated_list

auth = Blueprint('auth', __name__)

EXPIRE_REFRESH = datetime.timedelta(days=int(os.getenv('REFRESH_TOKEN_EXPIRED')))
EXPIRE_ACCESS = datetime.timedelta(hours=int(os.getenv('ACCESS_TOKEN_EXPIRED')))
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
AUTH_HISTORY_START_PAGE = os.getenv('AUTH_HISTORY_START_PAGE')
AUTH_HISTORY__PAGE_LIMIT = os.getenv('AUTH_HISTORY__PAGE_LIMIT')


class RegistrationAPI(Resource):
    """
    логика работы метода для регистрации нового пользователя api/auth/registration
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username")
    parser.add_argument('email', type=str, required=False, help="email")
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
            UserDataStore.register_user(username=body["username"], password=body["password"], email=body["email"])
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
                "message": "Username or password invalid"}}, HTTPStatus.UNAUTHORIZED
        # генерируем access и refresh токены
        superuser = False
        for role in RolesCRUD.check_user_role(user_id):
            if role.role_type == 'superuser':
                superuser = True
        access_token = TokenDataStore.create_jwt_token(
            username=body["username"], password=body["password"], user_id=user_id, expires_delta=EXPIRE_ACCESS,
            secret_key=SECRET_KEY, admin=superuser)
        refresh_token = TokenDataStore.create_refresh_token(
            username=body["username"], password=body["password"], user_id=user_id, expires_delta=EXPIRE_REFRESH,
            secret_key=SECRET_KEY, admin=superuser)
        # Проверяем наличие refresh токена в БД
        current_refresh = TokenDataStore.get_refresh_token(user_id=user_id)
        if current_refresh:
            return {"message": "User is authorized"}
        # заливаем refresh токен в БД
        TokenDataStore.save_refresh_token(refresh_token=refresh_token, user_id=user_id)
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
        # Проверка refresh tokena
        check_refresh_token = CheckAuthUser().check_access_token(token=body['refresh_token'])
        if check_refresh_token:
            # Проверяем access токен
            check_access_token = CheckAuthUser().check_access_token(token=body['refresh_token'])
            if check_access_token:
                return {"access_token": body['access_token'], "refresh_token": body['refresh_token']}
            else:
                # генерация новго access токена
                user_data = TokenDataStore.get_user_data_from_token(token=body['refresh_token'], secret_key=SECRET_KEY)
                new_access_token = TokenDataStore.create_jwt_token(
                    username=user_data["username"], password=user_data["password"], user_id=user_data["user_id"],
                    expires_delta=EXPIRE_ACCESS, secret_key=SECRET_KEY)
                return {"token": new_access_token, "refresh_token": body['refresh_token']}, HTTPStatus.OK


class LogoutAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('refresh_token', type=str, required=True, help="refresh_token")

    @staticmethod
    def post():
        body = request.get_json()
        refresh = Tokens.query.filter_by(refresh_token=body['refresh_token']).one_or_none()
        if refresh is None:
            return {"message": "Refresh token not valid"}, HTTPStatus.UNAUTHORIZED
        TokenDataStore.delete_refresh_token(refresh.refresh_token)
        return HTTPStatus.NO_CONTENT


class HistoryAuthAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('access_token', type=str, required=True, help="access_token")

    @staticmethod
    def get():
        body = request.get_json()
        check_access_token = CheckAuthUser().check_access_token(token=body['access_token'])
        if check_access_token:
            access_data = TokenDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
            return jsonify({"history": get_paginated_list(
                UserDataStore.get_user_history_auth(user_id=access_data['user_id']), '/api/v1/auth_history',
                start=request.args.get('start', AUTH_HISTORY_START_PAGE),
                limit=request.args.get('limit', AUTH_HISTORY__PAGE_LIMIT))})
        return {"access token not valid"}, HTTPStatus.UNAUTHORIZED


class ChangeAuthDataAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('new_username', type=str, help="login")
    parser.add_argument('new_password', type=str, help="password")
    parser.add_argument('access_token', type=str, required=True, help="access_token")

    @staticmethod
    def post():
        body = request.get_json()
        access_data = TokenDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
        check_access_token = CheckAuthUser().check_access_token(token=body['access_token'])
        if check_access_token:
            access_data = TokenDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
            return jsonify({"history": UserDataStore.get_user_history_auth(user_id=access_data['user_id'])})
        UserDataStore.change_user(user_id=access_data["user_id"], new_username=body["new_username"],
                                  new_password=body["new_password"])
