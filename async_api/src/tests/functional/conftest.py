import asyncio

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from typing import Optional

from tests.functional.settings import ELASTIC_HOST, ELASTIC_PORT, REDIS_HOST, REDIS_PORT, API_HOST, API_PORT, \
    API_VERSION
from tests.functional.utils.models import HTTPResponse
from tests.functional.testdata.test_data_film import TestDataFilm
from tests.functional.testdata.test_data_person import TestDataPerson
from tests.functional.testdata.test_data_genre import TestDataGenre


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch([f'{ELASTIC_HOST}: {ELASTIC_PORT}'], verify_certs=False)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding="utf-8", decode_responses=True)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session')
async def download_data_el_films(es_client):
    await es_client.bulk(index="movies", body=TestDataFilm.body_el, refresh=True)


@pytest.fixture(scope='session')
async def download_data_el_person(es_client):
    await es_client.bulk(index="person", body=TestDataPerson.body_el, refresh=True)


@pytest.fixture(scope='session')
async def download_data_el_genre(es_client):
    await es_client.bulk(index="genre", body=TestDataGenre.body_el, refresh=True)


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = f'{API_HOST}:{API_PORT}/api/{API_VERSION}/{method}'
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
