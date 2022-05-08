import grpc
from async_api.src.grpc_inegration.protobufs import user_check_pb2_grpc, user_check_pb2
import os


class CheckUsergRPCServices:

    GRPC_HOST = os.getenv("GRPC_HOST")
    GRPC_PORT = os.getenv("GRPC_PORT")

    @staticmethod
    def check_user_permission(token: str):
        channel = grpc.insecure_channel(f"{CheckUsergRPCServices.GRPC_HOST}:{CheckUsergRPCServices.GRPC_PORT}")
        client = user_check_pb2_grpc.CheckAuthUserStub(channel)
        request = user_check_pb2.CheckUserRequest(access_token=token)
        result = client.GetAuthInfo(request)
        return result

