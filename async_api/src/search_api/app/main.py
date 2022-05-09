import logging

import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from search_api.app.api.v1 import films, genres, persons
from search_api.app.core import config
from search_api.app.core.logger import LOGGING
from search_api.app.db import elastic, redis

app = FastAPI(

    title=config.PROJECT_NAME,

    docs_url='/api/openapi',

    openapi_url='/api/openapi.json',

    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.from_url(f'redis://{config.REDIS_HOST}', encoding="utf-8", decode_responses=True)
    elastic.es = AsyncElasticsearch(
        hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'],
        verify_certs=False)


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['film'])
app.include_router(genres.router, prefix='/api/v1/genre', tags=['genre'])
app.include_router(persons.router, prefix='/api/v1/person', tags=['person'])


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8010,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
