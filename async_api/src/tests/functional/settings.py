import os

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = os.getenv('ELASTIC_PORT', 9200)

API_HOST = os.getenv('API_HOST', 'http://127.0.0.1')
API_PORT = os.getenv('API_PORT', '8010')
API_VERSION = os.getenv('API_VERSION', 'v1')