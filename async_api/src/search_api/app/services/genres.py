import json
from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from search_api.app.db.elastic import get_elastic
from search_api.app.db.redis import get_redis
from search_api.app.models.genre_model import Genre
from search_api.app.services.cache import CacheService
from search_api.app.services.elastic import ElasticService


class GenreService(CacheService, ElasticService):

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_one_from_cache(genre_id)
        if not genre:
            genre = await self._get_one_from_elastic(genre_id, Genre, 'genre')
            if not genre:
                return None
            await self._put_to_cache(key=genre.id, value=genre.json())
        return genre

    async def get_all_genres(self, limit: int, sort_name: Optional[str] = None):
        genres_id = f"genres_id_{sort_name}&{limit}"
        genres = await self._get_all_from_cache(genres_id, Genre)
        if not genres:
            genres = await self._get_all_genre_from_elastic(limit=limit, sort_name=sort_name)
            if not genres:
                return None
            await self._put_to_cache(
                key=genres_id, value=json.dumps({"items": [genre.json() for genre in genres]})
            )
        return genres


@lru_cache
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)) -> GenreService:
    return GenreService(redis, elastic)
