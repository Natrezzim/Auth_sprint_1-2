import uuid
from http import HTTPStatus
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Header
from pydantic import BaseModel

from search_api.app.services.films import FilmService, get_film_service
from search_api.grpc_inegration.client.services import role_required

router = APIRouter()

ROLE_PERMISSION = "admin"


class Film(BaseModel):
    id: Optional[uuid.UUID]
    imdb_rating: Optional[float]
    genre: Optional[str]
    title: Optional[str]
    description: Optional[str]
    director: Optional[list[str]]
    actors: Optional[list[dict]]
    writers: Optional[list[dict]]


@router.get('/{film_id}', response_model=Film, summary="Поиск фильма по ID")
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    """
        Информация о фильме:
        - **id**: ID фильма
        - **imdb_rating**: IMDB рейтинг
        - **genre**: жанр фиьма
        - **title**: название фильма
        - **description**: полное описание фильма
        - **director**: режиссер фильма
        - **actors**: актеры принявшие участие в фильме
        - **writers**: сценаристы
    """
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(id=film.id, title=film.title, imdb_rating=film.imdb_rating, genre=film.genre,
                description=film.description, director=film.director, actors=film.actors, writers=film.writers)


@router.get('/', summary="Вывод всех имеющихся фильмов")
async def all_films(roles=Depends(role_required), film_service: FilmService = Depends(get_film_service),
                    limit: int = 10, genre: Optional[str] = None, actor: Optional[str] = None,
                    sort: Optional[str] = None) -> Dict:
    """
        Информация о фильме:

        - **id**: ID фильма
        - **imdb_rating**: IMDB рейтинг
        - **genre**: жанр фиьма
        - **title**: название фильма
        - **description**: полное описание фильма
        - **director**: режиссер фильма
        - **actors**: актеры принявшие участие в фильме
        - **writers**: сценаристы
    """
    if 'admin' not in roles:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Permission denied')
    films = await film_service.get_all_films(limit=limit, genre=genre, actor=actor, sort=sort)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
    film_list = [
        Film(id=film.id, title=film.title, imdb_rating=film.imdb_rating, genre=film.genre,
             description=film.description, director=film.director, actors=film.actors, writers=film.writers)
        for film in films
    ]

    result = {
        "count": len(film_list),
        "items": film_list
    }
    return result
