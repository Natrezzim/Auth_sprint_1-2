from .datastore import UserDataStore
from src.app.db.db_models import Tokens, Users
import os
import datetime


class CheckAuthUser:

    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY')

    def check_access_token(self, token: str):
        """
        Проверка валидности токена
        :param token: Токен
        :return:
        """
        # Получаем данные пользователя
        token_data = UserDataStore.get_user_data_from_token(token=token, secret_key=self.secret_key)
        # Проверяем наличие пользователя в БД
        check_user = Users.query.filter_by(user_id=token_data['user_id']).one_or_none()
        if check_user is None:
            return False
        # Проверяем срок действия токена
        current_time = datetime.datetime.now()
        expire_time_t = datetime.datetime.strptime(token_data["expires"], "%Y-%m-%dT%H:%M:%S")
        if current_time > expire_time_t:
            return False
        return True
