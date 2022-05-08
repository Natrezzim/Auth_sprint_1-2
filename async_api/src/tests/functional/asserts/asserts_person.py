from typing import Optional


class AssertsPerson:
    """
    Класс с проверками для тестов метода person
    """

    def assert_filter_role(self, resp_data: list, role: Optional[str] = None):
        """
        Проверка фильтра по роли
        :param resp_data:
        :param role:
        :return:
        """
        if role is not None:
            for person in resp_data:
                assert person['role'] == role, f"{person['role']} != {role}"

    def assert_sort_role(self, resp_data: list, sort: Optional[str] = None):
        """
        Проверка сортировки фильмов
        :param sort:
        :param resp_data:
        :return:
        """
        if sort is not None:
            reverse = True if sort == 'desc' else False
            role_list = [data['role'] for data in resp_data]
            assert role_list == sorted(role_list, reverse=reverse), \
                f"{role_list} != {sorted(role_list, reverse=reverse)}"

    def assert_sort_name(self, resp_data: list, sort: Optional[str] = None):
        """
        Проверка сортировки фильмов
        :param sort:
        :param resp_data:
        :return:
        """
        if sort is not None:
            reverse = True if sort == "desc" else False
            name_list = [data['name'] for data in resp_data]
            assert name_list == sorted(name_list, reverse=reverse), \
                f"{name_list} != {sorted(name_list, reverse=reverse)}"

