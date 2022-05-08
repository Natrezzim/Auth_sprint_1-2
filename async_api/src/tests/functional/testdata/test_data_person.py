import uuid


class TestDataPerson:

    body_el = [
        {"index": {"_id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"}},
        {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a", "name": "George Lucas", "role": "writer"},
        {"index": {"_id": "26e83050-29ef-4163-a99d-b546cac208f8"}},
        {"id": "26e83050-29ef-4163-a99d-b546cac208f8", "name": "Mark Hamill", "role": "director"},
        {"index": {"_id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1"}},
        {"id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1", "name": "Harrison Ford", "role": "actor"},
        {"index": {"_id": "f51f4731-3c26-4a72-9d68-cd0cd3d90a26"}},
        {"id": "f51f4731-3c26-4a72-9d68-cd0cd3d90a26", "name": "Ross Hagen", "role": "actor"},
        {"index": {"_id": "b258f144-d771-4fa2-b6a2-42805c13ce4a"}},
        {"id": "b258f144-d771-4fa2-b6a2-42805c13ce4a", "name": "Sandy Brooke", "role": "actor"}
    ]

    test_data = {
        "get_person_by_id": [
            (f"Получаем данные фильма по его id", {"id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
                                                   "exp_status_code": 200})
        ],
        "get_person_by_id_not_found": [
            (f"Получаем данные фильма по не существующему id", {"id": uuid.uuid4(),
                                                                "exp_status_code": 404})
        ],
        "get_list_persons": [
            (f"Получаем список фильмов", {"role": None, "sort_name": None, "sort_role": None, "limit": 10})
        ],
        "get_list_persons_filter_role": [
            (f"Получаем список фильмов фильтруя по полю role",
             {"role": "actor", "sort_name": None, "sort_role": None, "limit": 10})
        ],
        "get_list_persons_sort_role": [
            (f"Получаем список фильмов сортируя по полю role: asc",
             {"role": None, "sort_name": None, "sort_role": "asc", "limit": 10}),
            (f"Получаем список фильмов сортируя по полю role: desc",
             {"role": None, "sort_name": None, "sort_role": "desc", "limit": 10})
        ],
        "get_list_persons_sort_name": [
            (f"Получаем список фильмов сортируя по полю name: asc",
             {"role": None, "sort_name": "asc", "sort_role": None, "limit": 10}),
            (f"Получаем список фильмов сортируя по полю name: desc",
             {"role": None, "sort_name": "desc", "sort_role": None, "limit": 10})
        ]
    }
