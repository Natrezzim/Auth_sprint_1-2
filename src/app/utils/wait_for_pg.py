import logging
import os
from dotenv import load_dotenv
import backoff
import psycopg2

load_dotenv("../app/config/.env")

logging.getLogger('backoff').addHandler(logging.StreamHandler())

dsl = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST')
}


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=(psycopg2.Error, psycopg2.OperationalError))
def postgres_conn():
    psycopg2.connect(**dsl)


if __name__ == '__main__':
    postgres_conn()
