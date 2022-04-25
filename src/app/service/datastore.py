import datetime
import uuid

import jwt
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from src.app.db.db import db, session_scope
from src.app.db.db_models import AuthHistory, Tokens, UserPersonalData, Users


def password_encrypt(username: str, password: str):
    salt = str.encode(username)
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)
    key = kdf.derive(str.encode(password))
    password = str(key)
    return password


class UserDataStore:

    @staticmethod
    def authorize_user(username: str, password: str, user_agent: str):
        """
        Авторизация пользователя

        :param username: имя пользователя
        :param password: пароль
        :param user_agent: устройство
        :return: user_id: id пользователя
        """
        password = password_encrypt(username, password)
        user = Users.query.filter_by(username=username, password=password).one_or_none()
        if user is not None:
            auth_history = AuthHistory(id=uuid.uuid4(), user_id=user.id, user_agent=user_agent)
            with session_scope():
                db.session.add(auth_history)
            user_id = str(user.id)
            return user_id

    @staticmethod
    def register_user(username: str, password: str, email: str):
        """
        Регистрация пользователя

        :param username: имя пользователя
        :param password: пароль
        :param email: E-mail
        :return: user_id: id нового пользователя
        """
        new_user_id = uuid.uuid4()
        password = password_encrypt(username, password)
        new_user = Users(id=new_user_id, username=username, password=password)
        new_user_data = UserPersonalData(id=uuid.uuid4(), user_id=new_user_id, email=email)
        with session_scope():
            db.session.add(new_user)
            db.session.commit()
            db.session.add(new_user_data)
        new_created_user = Users.query.filter_by(id=new_user_id).one_or_none()
        if new_created_user is not None:
            new_id = str(new_created_user.id)
            return new_id
        return None

    @staticmethod
    def change_user(user_id, new_username: str, new_password: str):
        """
        Смена логина и пароля пользователя

        :param user_id: id пользователя
        :param username: имя пользователя
        :param password: пароль
        :return: user_id: None
        """
        user = Users.query.filter_by(id=user_id).one_or_none()
        password = password_encrypt(new_username, new_password)
        if user is not None:
            with session_scope():
                Users.query.filter_by(id=user.id).update({'username': new_username, 'password': password})
            return user.id
        return None

    @staticmethod
    def create_jwt_token(user_id: uuid.UUID, username: str, password: str, secret_key: str,
                         expires_delta: datetime.timedelta) -> str:
        """
        Создание jwt token

        :param user_id:
        :param username: имя пользователя
        :param password: пароль
        :param secret_key: подпись токена
        :param expires_delta: время действия токена
        :return:
        """
        current_time = datetime.datetime.now()
        expiries_time = current_time + expires_delta
        payload = {
            "user_id": user_id,
            "username": username,
            "password": password,
            "expires": expiries_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "type": "access"
        }
        token = jwt.encode(
            payload=payload,
            key=secret_key
        )
        return token

    @staticmethod
    def create_refresh_token(username: str, password: str, secret_key: str, expires_delta: datetime.timedelta,
                             user_id) -> str:
        """
        Создание refresh token

        :param user_id:
        :param username: имя пользователя
        :param password: пароль
        :param secret_key: подпись токена
        :param expires_delta: время действия токена
        :return:
        """
        current_time = datetime.datetime.now()
        expiries_time = current_time + expires_delta
        payload = {
            "user_id": user_id,
            "username": username,
            "password": password,
            "expires": expiries_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "type": "refresh"
        }
        token = jwt.encode(
            payload=payload,
            key=secret_key
        )
        return token

    @staticmethod
    def get_user_data_from_token(token: str, secret_key: str):
        """
        Получаем информацию о пользователе из jwt токена

        :param token:
        :param secret_key:
        :return:
        """
        data = jwt.decode(jwt=token, key=secret_key, algorithms="HS256")
        return data

    @staticmethod
    def save_refresh_token(refresh_token: str, user_id):
        """
        Сохраняет refresh token в БД

        :param refresh_token:
        :param user_id:
        :return:
        """
        token_info = Tokens(id=uuid.uuid4(), user_id=user_id, refresh_token=refresh_token)
        with session_scope():
            db.session.add(token_info)
            db.session.commit()

    @staticmethod
    def delete_refresh_token(refresh_token: str):
        """
        Сохраняет refresh token в БД

        :param refresh_token:
        :param user_id:
        :return:
        """
        token_info = Tokens.query.filter_by(refresh_token=refresh_token)
        with session_scope():
            db.session.remove(token_info)
            db.session.commit()
