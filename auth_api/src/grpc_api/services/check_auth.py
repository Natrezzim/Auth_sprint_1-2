import grpc
import os
import logging
from src.data.db.db import session_db
from src.data.db.db_models import Users, UserRole, Role
from src.data.datastore.token_datastore import TokenDataStore
from src.grpc_api.protobuf.user_check_pb2 import CheckUser
from src.grpc_api.protobuf import user_check_pb2_grpc
SECRET_KEY='t1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
# SECRET_KEY = os.getenv('JWT_SECRET_KEY')
import datetime

LOGGER = logging.getLogger(__name__)


class CheckAuthData:

    def check_available_user(self, user_id: str):
        with session_db() as s:
            check_user = s.query(Users).filter_by(id=user_id).one_or_none()
            return check_user

    def check_token_expired(self, exp):
        current_time = datetime.datetime.now()
        expire_time_t = datetime.datetime.strptime(exp, "%Y-%m-%dT%H:%M:%S")
        if current_time > expire_time_t:
            return False
        return True


class CheckAuthService(user_check_pb2_grpc.CheckAuthUserServicer, CheckAuthData):

    def GetAuthInfo(self, request, context):
        # Получаем данные пользователя
        token_data = TokenDataStore.get_user_data_from_token(token=request.access_token, secret_key=SECRET_KEY)
        # Проверяем наличие пользователя в БД
        if self.check_available_user(token_data["user_id"]) is None:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "access_token not valid")
        else:
            # Проверяем время жизни токена
            # if not self.check_token_expired(exp=token_data["expires"]):
            #     context.abort(grpc.StatusCode.UNAUTHENTICATED, "expired token")
            with session_db() as s:
                records = s.query(UserRole, Role).filter(
                    UserRole.user_id == token_data["user_id"],
                    UserRole.role_id == Role.id).all()
            check_user = CheckUser()
            check_user.status = 1
            if not records:
                try:
                    check_user.roles.append([])
                    return check_user
                except Exception as e:
                    print(e)
            for user_role, role in records:
                check_user.roles.append(role.role_type)
            return check_user
