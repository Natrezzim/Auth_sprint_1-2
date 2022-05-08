FROM python:3.9-alpine

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk add build-base && \
    apk --no-cache add curl && \
    pip install --upgrade pip && \
    pip install -U setuptools


COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8010

COPY . ./search_api
CMD ["uvicorn", "search_api.app.main:app", "--host", "0.0.0.0", "--port", "8010"]