from typing import Optional

class AssertsFilms:
    """
    Класс с проверками для тестов метода films
    """

    def assert_limit(self, exp_count: int, limit: int):
        """
        Проверка работы фильтра limit
        :param exp_count:
        :param limit:
        :return:
        """
        if limit is not None:
            assert exp_count == limit, f"{exp_count} != {limit}"

    def assert_sort_rating(self, resp_data: list, sort: Optional[str] = None):
        """
        Проверка сортировки фильмов
        :param sort:
        :param resp_data:
        :return:
        """
        if sort is not None:
            reverse = True if [w for w in sort][0] == '-' else False
            rating_list = [rating['imdb_rating'] for rating in resp_data]
            assert rating_list == sorted(rating_list, reverse=reverse), \
                f"{rating_list} != {sorted(rating_list, reverse=reverse)}"

    def assert_filter_genre(self, resp_data: list, genre: Optional[str] = None):
        """
        Проверка фильтра по жанру
        :param resp_data:
        :param genre:
        :return:
        """
        if genre is not None:
            for film in resp_data:
                assert film['genre'] == genre, f"{film['genre']} != {genre}"

    def assert_filter_person(self, resp_data: list, person: Optional[str] = None):
        """
        Проверка фильтра по жанру
        :param resp_data:
        :param person:
        :return:
        """
        if person is not None:
            for film in resp_data:
                count = 0
                for actor in film["actors"]:
                    print(actor["name"])
                    if actor["name"] == person:
                        count += 1
                for writer in film["writers"]:
                    print(writer["name"])
                    if writer["name"] == person:
                        count += 1
                assert count > 0, f"Ожидаемый человек с именем: {person} отсутсвует в информации о фильме"

