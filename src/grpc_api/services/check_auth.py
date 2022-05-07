import grpc
import os

from src.data.check_user import CheckAuthUser
from src.data.datastore.roles_datastore import RolesCRUD
from src.data.datastore.token_datastore import TokenDataStore
from src.grpc_api.protobuf.user_check_pb2 import (CheckUserRequest, CheckUser, RoleUser)
from src.grpc_api.protobuf import user_check_pb2_grpc
SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class CheckAuthService(user_check_pb2_grpc.CheckAuthUserServicer):

    def user_data(self, request, context):
        check_access_token = CheckAuthUser().check_access_token(token=request.access_token)
        if check_access_token:
            access_data = TokenDataStore.get_user_data_from_token(token=request.access_token, secret_key=SECRET_KEY)
            user_roles = RolesCRUD.check_user_role(access_data["user_id"])
            return CheckUser(status=True, role=user_roles)
        else:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "access_token not valid")
