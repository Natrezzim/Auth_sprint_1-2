from search_api.app.models.base_model import BaseModelMixin


class Person(BaseModelMixin):
    id: str
    name: str
    role: str
