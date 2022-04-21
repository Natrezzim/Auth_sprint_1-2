FROM python:3.9-alpine

WORKDIR /usr

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add build-base && \
    apk --no-cache add curl && \
    pip install --upgrade pip && \
    pip install -U setuptools
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

COPY . ./src