import logging
from functools import lru_cache
from typing import Optional
import json

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from search_api.app.db.elastic import get_elastic
from search_api.app.db.redis import get_redis
from search_api.app.models.person_model import Person
from search_api.app.services.cache import CacheService
from search_api.app.services.elastic import ElasticService

LOGGER = logging.getLogger(__name__)


class PersonService(CacheService, ElasticService):

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._get_one_from_cache(person_id)
        if not person:
            person = await self._get_one_from_elastic(person_id, Person, 'person')
            if not person:
                return None
            await self._put_to_cache(key=person.id, value=person.json())
        return person

    async def get_all_persons(self, limit: int, role: Optional[str] = None, sort_name: Optional[str] = None,
                              sort_role: Optional[str] = None):
        persons_id = f"persons_id_{role}&{sort_name}&{sort_role}&{limit}"
        persons = await self._get_all_from_cache(persons_id, Person)
        if not persons:
            persons = await self._get_all_person_from_elastic(limit=limit, role=role, sort_name=sort_name,
                                                              sort_role=sort_role)
            if not persons:
                return None
            await self._put_to_cache(
                key=persons_id, value=json.dumps({"items": [person.json() for person in persons]})
            )
        return persons


@lru_cache
def get_person_service(redis: Redis = Depends(get_redis),
                       elastic: AsyncElasticsearch = Depends(get_elastic)) -> PersonService:
    return PersonService(redis, elastic)
