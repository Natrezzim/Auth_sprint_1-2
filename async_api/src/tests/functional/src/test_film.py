import pytest
import logging
from tests.functional.testdata.test_data_film import TestDataFilm
from tests.functional.asserts.asserts_films import AssertsFilms
from tests.functional.utils.common import UtilsCommon


LOGGER = logging.getLogger(__name__)

pytestmark = [pytest.mark.all_tests]


@pytest.mark.usefixtures("download_data_el_films")
class TestsFilm:

    def setup_class(self):
        self.exp_data = [i for i in TestDataFilm.body_el[1::2]]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataFilm.test_data['films_positive'])
    async def test_check_all_films_not_filter(self, es_client, make_get_request, test_title, redis_client, test_data):
        films_id = f"films_id_{test_data['params']['genre']}&{test_data['params']['actor']}&" \
                   f"{test_data['params']['sort']}&{test_data['params']['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data["params"])
        # запрашиваем данные из el в созданном индексе с параметрами test_data["params"]
        response = await make_get_request(method='films', params=params)
        assert response.status == 200
        assert response.body.get("count") == len(response.body.get("items"))
        # Проверяем наличие данных в redis
        redis_result = await redis_client.get(films_id)
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataFilm.test_data['filter_limit'])
    async def test_check_all_films_filter_limit(self, es_client, make_get_request, test_title, redis_client, test_data):
        films_id = f"films_id_{test_data['params']['genre']}&{test_data['params']['actor']}&" \
                   f"{test_data['params']['sort']}&{test_data['params']['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data["params"])
        # запрашиваем данные из el в созданном индексе с параметрами test_data["params"]
        response = await make_get_request(method='films', params=params)
        assert response.status == 200
        assert response.body.get("count") == len(response.body.get("items"))
        # проверка фильтра limit
        AssertsFilms().assert_limit(exp_count=response.body.get("count"), limit=test_data["params"]["limit"])
        # Проверяем наличие данных в redis
        redis_result = await redis_client.get(films_id)
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataFilm.test_data['filter_imdb_rating'])
    async def test_check_all_films_sort_rating(self, es_client, make_get_request, test_title, redis_client, test_data):
        films_id = f"films_id_{test_data['params']['genre']}&{test_data['params']['actor']}&" \
                   f"{test_data['params']['sort']}&{test_data['params']['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data["params"])
        # запрашиваем данные из el в созданном индексе с параметрами test_data["params"]
        response = await make_get_request(method='films', params=params)
        assert response.status == 200
        assert response.body.get("count") == len(response.body.get("items"))
        # проверка работы сортировки
        AssertsFilms().assert_sort_rating(sort=test_data["params"]["sort"], resp_data=response.body.get("items"))
        # Проверяем наличие данных в redis
        redis_result = await redis_client.get(films_id)
        assert redis_result is not None


    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataFilm.test_data['filter_genre'])
    async def test_check_all_films_filter_genre(self, es_client, make_get_request, test_title, redis_client, test_data):
        films_id = f"films_id_{test_data['params']['genre']}&{test_data['params']['actor']}&" \
                   f"{test_data['params']['sort']}&{test_data['params']['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data["params"])
        # запрашиваем данные из el в созданном индексе с параметрами test_data["params"]
        response = await make_get_request(method='films', params=params)
        assert response.status == 200
        assert response.body.get("count") == len(response.body.get("items"))
        # Проверка фильтрации по полю  genre
        AssertsFilms().assert_filter_genre(genre=test_data["params"]['genre'], resp_data=response.body.get("items"))
        # Проверяем наличие данных в redis
        redis_result = await redis_client.get(films_id)
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataFilm.test_data['filter_person'])
    async def test_check_all_films_filter_person(self, es_client, make_get_request, test_title, redis_client, test_data):
        films_id = f"films_id_{test_data['params']['genre']}&{test_data['params']['actor']}&" \
                   f"{test_data['params']['sort']}&{test_data['params']['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data["params"])
        # запрашиваем данные из el в созданном индексе с параметрами test_data["params"]
        response = await make_get_request(method='films', params=params)
        assert response.status == 200
        assert response.body.get("count") == len(response.body.get("items"))
        # Проверка фильтрации по полю person
        AssertsFilms().assert_filter_person(person=test_data["params"]['actor'], resp_data=response.body.get("items"))
        # Проверяем наличие данных в redis
        redis_result = await redis_client.get(films_id)
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataFilm.test_data['get_film_id_positive'])
    async def test_check_film_by_id(self, es_client, make_get_request, test_title, redis_client, test_data):
        method = f"films/{test_data['id']}"
        response = await make_get_request(method=method)
        assert response.status == 200
        assert response.body.get("id") == test_data['id']
        # Проверяем наличие данных в redis
        redis_result = await redis_client.get(response.body.get("id"))
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataFilm.test_data['get_film_id_not_found'])
    async def test_check_film_by_id_not_found(self, es_client, make_get_request, test_title, redis_client, test_data):
        method = f"films/{test_data['id']}"
        response = await make_get_request(method=method)
        assert response.status == 404
