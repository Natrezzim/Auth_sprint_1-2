import uuid
from http import HTTPStatus
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from search_api.app.services.genres import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str]


@router.get('/{genre_id}', response_model=Genre, summary="Поиск жанров по ID")
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    """
        Информация о жанре:

        - **id**: ID жанра
        - **name**: название жанра
    """
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return Genre(id=genre.id, name=genre.name)


@router.get('/', summary="Вывод всех имеющихся жанров")
async def all_genres(genre_service: GenreService = Depends(get_genre_service), limit: int = 10,
                     sort_name: Optional[str] = None) -> Dict:
    """
        Информация о жанре:

        - **id**: ID жанра
        - **name**: название жанра
    """
    genres = await genre_service.get_all_genres(limit=limit, sort_name=sort_name)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    genre_list = [
        Genre(id=genre.id, name=genre.name)
        for genre in genres
    ]

    result = {
        "count": len(genre_list),
        "items": genre_list
    }
    return result
