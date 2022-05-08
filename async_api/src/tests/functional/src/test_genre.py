import pytest
from tests.functional.testdata.test_data_genre import TestDataGenre
from tests.functional.utils.common import UtilsCommon
from tests.functional.asserts.asserts_person import AssertsPerson

pytestmark = [pytest.mark.all_tests]


@pytest.mark.usefixtures("download_data_el_genre")
class TestsGenre:

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataGenre.test_data['get_genre_by_id'])
    async def test_genre_by_id(self, test_title, test_data, es_client, make_get_request, redis_client):
        method = f"genre/{test_data['id']}"
        response = await make_get_request(method=method)
        assert response.status == test_data["exp_status_code"]
        assert response.body.get("id") == test_data["id"]
        # проверка даннных в redis
        redis_result = await redis_client.get(response.body.get("id"))
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataGenre.test_data['get_genre_by_id_not_found'])
    async def test_search_genre_by_id_not_found(self, test_title, test_data, es_client, make_get_request,
                                                 redis_client):
        method = f"genre/{test_data['id']}"
        response = await make_get_request(method=method)
        assert response.status == test_data["exp_status_code"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataGenre.test_data['get_list_genres'])
    async def test_search_list_genres(self, test_data, test_title, es_client, make_get_request, redis_client):
        cache_id = f"genres_id_{test_data['sort_name']}&{test_data['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data)
        response = await make_get_request(method='genre', params=params)
        assert response.status == 200
        assert response.body.get("count") == len(TestDataGenre.body_el[1::2])
        # проверка даннных в redis
        redis_result = await redis_client.get(cache_id)
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataGenre.test_data['get_list_genres_limit'])
    async def test_search_list_genres_limit(self, test_data, test_title, es_client, make_get_request, redis_client):
        cache_id = f"genres_id_{test_data['sort_name']}&{test_data['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data)
        response = await make_get_request(method='genre', params=params)
        assert response.status == 200
        assert response.body.get("count") == test_data['limit']
        # проверка даннных в redis
        redis_result = await redis_client.get(cache_id)
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataGenre.test_data['get_list_genres_sort_name'])
    async def test_search_list_genre_sort_name(self, test_data, test_title, es_client, make_get_request,
                                                 redis_client):
        cache_id = f"genres_id_{test_data['sort_name']}&{test_data['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data)
        response = await make_get_request(method='genre', params=params)
        assert response.status == 200
        AssertsPerson().assert_sort_name(resp_data=response.body.get("items"), sort=test_data["sort_name"])
        # проверка даннных в redis
        redis_result = await redis_client.get(cache_id)
        assert redis_result is not None
