import json
import logging
from typing import Optional, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch

CACHE_EXPIRE_IN_SECONDS = 60 * 5
LOGGER = logging.getLogger(__name__)


class CacheService:

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def _put_to_cache(self, key: str, value: Union[str, dict, list]):
        await self.redis.set(key, value, ex=CACHE_EXPIRE_IN_SECONDS)

    async def _get_one_from_cache(self, key: str) -> Optional:
        data = await self.redis.get(key)
        LOGGER.info(f'Data from Redis {data}')
        if not data:
            return None

    async def _get_all_from_cache(self, key: str, model):
        data = await self.redis.get(key)
        if not data:
            return None
        LOGGER.info(f'Data from Redis {data}')
        index = [model.parse_raw(d) for d in json.loads(data)['items']]
        return index

    async def _film_from_cache(self, key: str, model):
        data = await self.redis.get(key)
        if not data:
            return None
        LOGGER.info(f'Data from Redis {data}')
        index = model.parse_raw(data)
        return index
