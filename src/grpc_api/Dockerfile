FROM python:3.9-alpine

WORKDIR /usr

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk add build-base && \
    apk --no-cache add curl && \
    apk add --no-cache \
        libressl-dev \
        musl-dev \
        libffi-dev && \
    pip install --upgrade pip && \
    pip install -U setuptools


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./data ./src/data
COPY ./grpc_api ./src/grpc_api
RUN python -m grpc_tools.protoc -I ./src/grpc_api/protobuf --python_out=. \
           --grpc_python_out=. ./src/grpc_api/protobuf/user_check.proto \

# ENTRYPOINT [ "python", "src/grpc/main.py" ]