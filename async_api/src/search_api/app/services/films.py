import logging
from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends
import json

from search_api.app.db.elastic import get_elastic
from search_api.app.db.redis import get_redis
from search_api.app.models.film_model import Film
from search_api.app.services.cache import CacheService
from search_api.app.services.elastic import ElasticService

LOGGER = logging.getLogger(__name__)


class FilmService(CacheService, ElasticService):

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id, Film)
        if not film:
            film = await self._get_one_from_elastic(film_id, Film, 'movies')
            if not film:
                return None
            await self._put_to_cache(key=film.id, value=film.json())
        return film

    async def get_all_films(self, limit: int, genre: Optional[str] = None, actor: Optional[str] = None,
                            sort: Optional[str] = None):
        films_id = f"films_id_{genre}&{actor}&{sort}&{limit}"
        films = await self._get_all_from_cache(films_id, Film)
        if not films:
            films = await self._get_all_film_from_elastic(limit=limit, genre=genre, actor=actor, sort=sort)
            if not films:
                return None
            await self._put_to_cache(key=films_id, value=json.dumps({"items": [film.json() for film in films]}))
        return films


@lru_cache
def get_film_service(redis: Redis = Depends(get_redis),
                     elastic: AsyncElasticsearch = Depends(get_elastic)) -> FilmService:
    return FilmService(redis, elastic)
