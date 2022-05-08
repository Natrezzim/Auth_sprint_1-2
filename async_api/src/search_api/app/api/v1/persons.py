import logging
import uuid
from http import HTTPStatus
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from search_api.app.services.persons import PersonService, get_person_service

router = APIRouter()

LOGGER = logging.getLogger(__name__)


class Person(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str]
    role: Optional[str]


@router.get('/{person_id}', response_model=Person, summary="Поиск персон по ID")
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    """
        Информация о актере:

        - **id**: ID персоны
        - **name**: имя персоны
        - **role**: роль персоны
    """
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(id=person.id, name=person.name, role=person.role)


@router.get('/', summary="Вывод всех имеющихся персон")
async def all_persons(person_service: PersonService = Depends(get_person_service), limit: int = 10,
                      role: Optional[str] = None, sort_role: Optional[str] = None, sort_name: Optional[str] = None) -> Dict:
    """
        Информация о актере:

        - **id**: ID персоны
        - **name**: имя персоны
        - **role**: роль персоны
    """
    persons = await person_service.get_all_persons(limit=limit, role=role, sort_role=sort_role, sort_name=sort_name)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    LOGGER.info([(person.id, person.name, person.role) for person in persons])
    person_list = [
        Person(id=person.id, name=person.name, role=person.role)
        for person in persons
    ]

    result = {
        "count": len(person_list),
        "items": person_list
    }
    return result
