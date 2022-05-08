FROM python:3.9-alpine

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="${PYTHONPATH}:/tests"
RUN apk update && \
    apk add build-base && \
    apk --no-cache add curl && \
    pip install --upgrade pip && \
    pip install -U setuptools
COPY ./tests/functional/requirements.txt .
RUN pip install -r requirements.txt
COPY ./tests ./tests
COPY ./online_cinema/postgres_to_elastic/create_elastic_schema.sh ./tests/functional/testdata
CMD sh /usr/src/tests/functional/testdata/create_elastic_schema.sh
