from concurrent import futures
from protobuf import user_check_pb2_grpc
from src.grpc_api.services.check_auth import CheckAuthService
from src.data.db import db

import grpc


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_check_pb2_grpc.add_CheckAuthUserServicer_to_server(
        CheckAuthService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    run()