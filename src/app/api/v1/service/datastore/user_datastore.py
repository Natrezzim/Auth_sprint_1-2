import datetime
import uuid

import jwt
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from src.app.db.db import db, session_scope
from src.app.db.db_models import AuthHistory, Tokens, UserPersonalData, Users
from sqlalchemy import update, delete


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
        :param new_username: имя пользователя
        :param new_password: пароль
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
    def get_user_history_auth(user_id: str):
        """
        Получить историю входов в акккаунт пользователя
        :param user_id:
        :return:
        """
        history_auth = AuthHistory.query.filter(AuthHistory.user_id == user_id).all()

        return history_auth

    @staticmethod
    def change_login_user(user_id: str, new_username: str):
        """
        Изменить login пользователя
        :param new_username:
        :param user_id:
        :return:
        """
        stmt = update(Users).where(Users.user_id == user_id).values(username=new_username). \
            execution_options(synchronize_session="fetch")
        with session_scope():
            db.session.execute(stmt)
            db.session.commit()

    @staticmethod
    def change_password_user(user_id: str, new_password: str):
        """
        Изменить password пользователя
        :param new_password:
        :param user_id:
        :return:
        """
        stmt = update(Users).where(Users.user_id == user_id).values(password=new_password). \
            execution_options(synchronize_session="fetch")
        with session_scope():
            db.session.execute(stmt)
            db.session.commit()
