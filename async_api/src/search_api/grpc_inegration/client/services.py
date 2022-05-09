
import grpc
from search_api.grpc_inegration.protobufs import user_check_pb2_grpc, user_check_pb2
import os
from fastapi import Header
from http import HTTPStatus
from typing import Optional
from dotenv import load_dotenv

load_dotenv(f'{os.getcwd()}/search_api/app/.env')


class CheckUsergRPCServices:

    GRPC_HOST = "127.0.0.1"
    GRPC_PORT = "50051"

    @staticmethod
    def check_user_permission(token: str):
        channel = grpc.insecure_channel(f"{CheckUsergRPCServices.GRPC_HOST}:{CheckUsergRPCServices.GRPC_PORT}")
        client = user_check_pb2_grpc.CheckAuthUserStub(channel)
        request = user_check_pb2.CheckUserRequest(access_token=token)
        result = client.GetAuthInfo(request)
        return result


def role_required(x_access_token: Optional[str] = Header(...)):

    if x_access_token:
        token = x_access_token
    else:
        return {"message": "Missing access token. Expected x-access-token headers"}, HTTPStatus.UNAUTHORIZED
    if not token:
        return {"message": "A valid token is missing!"}, HTTPStatus.UNAUTHORIZED
    roles = CheckUsergRPCServices().check_user_permission(token=token)
    return roles



# def role_required(access_role: str = "admin"):
#     def func_wrapper(f):
#         @wraps(f)
#         async def decorator(*args, request: Request, **kwargs):
#             token = None
#             if 'x-access-token' in request.headers:
#                 token = request.headers.get('x-access-token')
#             else:
#                 return {"message": "Missing access token. Expected x-access-token headers"}, HTTPStatus.UNAUTHORIZED
#             if not token:
#                 return {"message": "A valid token is missing!"}, HTTPStatus.UNAUTHORIZED
#             roles = CheckUsergRPCServices().check_user_permission(token=token)
#             if access_role not in roles:
#                 return HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Permission denied')
#             return await f(*args, **kwargs)
#
#         return decorator
#
#     return func_wrapper
