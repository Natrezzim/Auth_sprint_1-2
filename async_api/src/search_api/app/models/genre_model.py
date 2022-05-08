from search_api.app.models.base_model import BaseModelMixin


class Genre(BaseModelMixin):
    id: str
    name: str
