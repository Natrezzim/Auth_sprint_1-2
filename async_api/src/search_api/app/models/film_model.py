from typing import Optional

from search_api.app.models.base_model import BaseModelMixin


class Film(BaseModelMixin):
    id: str
    title: Optional[str]
    description: Optional[str]
    imdb_rating: Optional[float]
    genre: Optional[str]
    director: Optional[list[str]]
    actors: Optional[list[dict]]
    writers: Optional[list[dict]]
