import logging
from typing import Optional

from elasticsearch import AsyncElasticsearch, exceptions

from search_api.app.models.genre_model import Genre
from search_api.app.models.film_model import Film
from search_api.app.models.person_model import Person

LOGGER = logging.getLogger(__name__)


class ElasticService:

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def _get_one_from_elastic(self, film_id: str, model, index: str) -> Optional:
        try:
            doc = await self.elastic.get(index=index, id=film_id)
        except exceptions.NotFoundError:
            return None
        return model(**doc['_source'])

    async def _get_all_film_from_elastic(
            self, limit: int, genre: Optional[str] = None, actor: Optional[str] = None,
            sort: Optional[str] = None
    ) -> Optional[list[Film]]:
        if genre or actor or sort:
            query = await self._get_films_query(actor=actor, genre=genre, sort=sort)
        else:
            query = None
        try:
            films = await self.elastic.search(index='movies', size=limit, body=query)
        except exceptions.NotFoundError:
            return None
        return [Film(**film['_source']) for film in films['hits']['hits']]

    async def _get_all_person_from_elastic(
            self, limit: int, role: Optional[str] = None, sort_role: Optional[str] = None,
            sort_name: Optional[str] = None) -> Optional[list[Person]]:

        if role or sort_role or sort_name is not None:
            query = await self._get_persons_query(sort_role=sort_role, sort_name=sort_name, role=role)
        else:
            query = None
        try:
            persons = await self.elastic.search(index='person', size=limit, body=query)
        except exceptions.NotFoundError:
            return None
        return [Person(**person['_source']) for person in persons['hits']['hits']]

    async def _get_all_genre_from_elastic(self, limit: int, sort_name: Optional[str] = None) -> Optional[list[Genre]]:
        query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        if sort_name is not None:
            query.update(
                {"sort": [{"name": {"order": sort_name, "unmapped_type": "long"}}]})
        try:
            genres = await self.elastic.search(index='genre', size=limit, body=query)
        except exceptions.NotFoundError:
            return None
        return [Genre(**genre['_source']) for genre in genres['hits']['hits']]

    @staticmethod
    async def _get_films_query(actor, genre, sort):
        query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        if sort:
            sort_type = "desc" if sort.startswith("-") else "asc"
            sort_field = sort.removeprefix("-")
        if actor or genre:
            if actor is not None:
                query['query']['bool']["must"].append({
                    "nested": {
                        "path": "actors",
                        'query': {
                            'bool': {
                                'must': [{"query_string": {"default_field": "actors.name", "query": f"*{actor}*"}}]
                            }
                        }
                    }
                }
                )
            if genre is not None:
                query['query']["bool"]['must'].append({
                    "query_string": {"default_field": "genre", "query": f"*{genre}*"}
                })
            if sort:
                query.update({"sort": [{sort_field: {"order": sort_type, "unmapped_type": "long"}}]})
        elif sort:
            query = {"query": {
                "match_all": {}
            },
                "sort": [{sort_field: {"order": sort_type, "unmapped_type": "long"}}]
            }
        LOGGER.info(query)
        return query

    @staticmethod
    async def _get_persons_query(role: Optional[str] = None, sort_role: Optional[str] = None,
                                 sort_name: Optional[str] = None):
        query = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        if role is not None:
            query['query']["bool"]['must'].append({
                "query_string": {"default_field": "role", "query": f"*{role}*"}
            })
            if sort_role is not None or sort_name is not None:
                query.update({"sort": []})
                if sort_role is not None:
                    query["sort"].append({"role": {"order": sort_role, "unmapped_type": "long"}})
                if sort_name is not None:
                    query["sort"].append({"name": {"order": sort_name, "unmapped_type": "long"}})
        elif sort_role is not None or sort_name is not None:
            query = {"query": {
                "match_all": {}
            },
                "sort": []
            }
            if sort_role is not None:
                query["sort"].append({"role": {"order": sort_role, "unmapped_type": "long"}})
            if sort_name is not None:
                query["sort"].append({"name": {"order": sort_name, "unmapped_type": "long"}})
        LOGGER.info(query)
        return query
