import uuid


class TestDataGenre:
    body_el = [
        {"index": {"_id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"}},
        {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
        {"index": {"_id": "120a21cf-9097-479e-904a-13dd7198c1dd"}},
        {"id": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"},
        {"index": {"_id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd"}},
        {"id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy"},
        {"index": {"_id": "6c162475-c7ed-4461-9184-001ef3d9f26e"}},
        {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
        {"index": {"_id": "1cacff68-643e-4ddd-8f57-84b62538081a"}},
        {"id": "1cacff68-643e-4ddd-8f57-84b62538081a", "name": "Drama"},
        {"index": {"_id": "56b541ab-4d66-4021-8708-397762bff2d4"}},
        {"id": "56b541ab-4d66-4021-8708-397762bff2d4", "name": "Music"}
    ]

    test_data = {
        "get_genre_by_id": [
            (f"Получаем данные фильма по его id", {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                                                   "exp_status_code": 200})
        ],
        "get_genre_by_id_not_found": [
            (f"Получаем данные фильма по не существующему id", {"id": uuid.uuid4(),
                                                                "exp_status_code": 404})
        ],
        "get_list_genres": [
            (f"Получаем список фильмов", {"sort_name": None, "limit": 10})
        ],
        "get_list_genres_limit": [
            (f"Получаем список фильмов c лимитом", {"sort_name": None, "limit": 2})
        ],
        "get_list_genres_sort_name": [
            (f"Получаем список фильмов сортируя по полю name: asc",
             {"sort_name": "asc", "limit": 10}),
            (f"Получаем список фильмов сортируя по полю name: desc",
             {"sort_name": "desc", "limit": 10})
        ]
    }

