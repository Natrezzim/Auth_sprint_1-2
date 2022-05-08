import pytest
from tests.functional.testdata.test_data_person import TestDataPerson
from tests.functional.utils.common import UtilsCommon
from tests.functional.asserts.asserts_person import AssertsPerson

pytestmark = [pytest.mark.all_tests]


@pytest.mark.usefixtures("download_data_el_person")
class TestsPerson:

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataPerson.test_data['get_person_by_id'])
    async def test_search_person_by_id(self, test_title, test_data, es_client, make_get_request, redis_client):
        method = f"person/{test_data['id']}"
        response = await make_get_request(method=method)
        assert response.status == test_data["exp_status_code"]
        assert response.body.get("id") == test_data["id"]
        # проверка даннных в redis
        redis_result = await redis_client.get(response.body.get("id"))
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataPerson.test_data['get_person_by_id_not_found'])
    async def test_search_person_by_id_not_found(self, test_title, test_data, es_client, make_get_request, redis_client):
        method = f"person/{test_data['id']}"
        response = await make_get_request(method=method)
        assert response.status == test_data["exp_status_code"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataPerson.test_data['get_list_persons'])
    async def test_search_list_persons(self, test_data, test_title, es_client, make_get_request, redis_client):
        cache_id = f"persons_id_{test_data['role']}&{test_data['sort_name']}&{test_data['sort_role']}&{test_data['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data)
        response = await make_get_request(method='person', params=params)
        assert response.status == 200
        assert response.body.get("count") == len(TestDataPerson.body_el[1::2])
        # проверка даннных в redis
        redis_result = await redis_client.get(cache_id)
        assert redis_result is not None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataPerson.test_data['get_list_persons_filter_role'])
    async def test_search_list_persons_role_filter(self, test_data, test_title, es_client, make_get_request,
                                                   redis_client):
        cache_id = f"persons_id_{test_data['role']}&{test_data['sort_name']}&{test_data['sort_role']}&{test_data['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data)
        response = await make_get_request(method='person', params=params)
        assert response.status == 200
        AssertsPerson().assert_filter_role(resp_data=response.body.get("items"), role=test_data["role"])
        # проверка даннных в redis
        redis_result = await redis_client.get(cache_id)
        assert redis_result is not None

    @pytest.mark.asyncio
    async def test_search_list_persons_role_filter_not_found(self, es_client, make_get_request,
                                                             redis_client):
        params = {"role": "test"}
        response = await make_get_request(method='person', params=params)
        assert response.status == 404

    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataPerson.test_data['get_list_persons_sort_role'])
    async def test_search_list_persons_sort_role(self, test_data, test_title, es_client, make_get_request,
                                                 redis_client):
        cache_id = f"persons_id_{test_data['role']}&{test_data['sort_name']}&{test_data['sort_role']}&{test_data['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data)
        response = await make_get_request(method='person', params=params)
        assert response.status == 200
        AssertsPerson().assert_sort_role(resp_data=response.body.get("items"), sort=test_data["sort_role"])
        # проверка даннных в redis
        redis_result = await redis_client.get(cache_id)
        assert redis_result is not None

    @pytest.mark.skip(f"Сортировка не коректно работает c различным регистором букв")
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_title, test_data", TestDataPerson.test_data['get_list_persons_sort_name'])
    async def test_search_list_persons_sort_name(self, test_data, test_title, es_client, make_get_request,
                                                 redis_client):
        cache_id = f"persons_id_{test_data['role']}&{test_data['sort_name']}&{test_data['sort_role']}&{test_data['limit']}"
        # создаём параметры для запроса на основании тестовых данных
        params = UtilsCommon().create_params(**test_data)
        response = await make_get_request(method='person', params=params)
        assert response.status == 200
        AssertsPerson().assert_sort_name(resp_data=response.body.get("items"), sort=test_data["sort_name"])
        # проверка даннных в redis
        redis_result = await redis_client.get(cache_id)
        assert redis_result is not None
