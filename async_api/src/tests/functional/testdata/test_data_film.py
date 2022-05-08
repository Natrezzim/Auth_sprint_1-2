import random
import uuid


class TestDataFilm:

    body_el = [
        {
            "index": {"_id": "00af52ec-9345-4d66-adbe-50eb917f463a"}
        },
        {
            "id": "00af52ec-9345-4d66-adbe-50eb917f463a",
            "imdb_rating": 3.5,
            "genre": "Sci-Fi",
            "title": "Star Slammer",
            "description": "Two women who have been unjustly confined to a prison planet plot their escape, all the "
                           "while having to put up with lesbian guards, crazed wardens and mutant rodents.",
            "director": [
                "Fred Olen Ray"
            ],
            "actors": [
                {
                    "id": "040147e3-0965-4117-8112-55a2087e0b84",
                    "name": "Marya Gant"
                },
                {
                    "id": "a91ff1c9-98a3-46af-a0d0-e9f2a2b4f51e",
                    "name": "Suzy Stokey"
                },
                {
                    "id": "b258f144-d771-4fa2-b6a2-42805c13ce4a",
                    "name": "Sandy Brooke"
                },
                {
                    "id": "f51f4731-3c26-4a72-9d68-cd0cd3d90a26",
                    "name": "Ross Hagen"
                }
            ],
            "writers": [
                {
                    "id": "82416ac7-26fa-40a6-a433-1c756c0fad6e",
                    "name": "Miriam L. Preissel"
                },
                {
                    "id": "a2fd6df4-9f3c-4a26-8d59-914470d2aea0",
                    "name": "Fred Olen Ray"
                },
                {
                    "id": "dac61d8f-f36e-4351-a4d8-9048b87d00a6",
                    "name": "Michael Sonye"
                }
            ]
        },
        {
            "index": {"_id": "89734888-0254-4040-b87c-30e2cb144d0d"}
        },
        {
            "id": "89734888-0254-4040-b87c-30e2cb144d0d",
            "imdb_rating": 8.1,
            "genre": "Sci-Fi",
            "title": "Star Wars: X-Wing",
            "description": "Be a Rebel pilot during the Galactic Civil War. Fly the most famous Star Wars starfighters "
                           "in furious battles against Imperial pilots.",
            "director": [],
            "actors": [
                {
                    "id": "087de4c7-8d61-4337-beae-d5ce3c440b00",
                    "name": "Nick Jameson"
                },
                {
                    "id": "bdd44e92-7498-445b-998e-0c2bd9591052",
                    "name": "Erik Bauersfeld"
                },
                {
                    "id": "ccf38643-1f0a-4b04-bcb5-dd27dde321f6",
                    "name": "Clive Revill"
                }
            ],
            "writers": [
                {
                    "id": "4d2b6d34-a5d7-46f8-8f42-80f754226c11",
                    "name": "Lawrence Holland"
                },
                {
                    "id": "567bedb8-982c-444a-af7d-df47cac1906d",
                    "name": "Edward Kilham"
                },
                {
                    "id": "e03e9083-891b-48c4-b075-4b39c45979ac",
                    "name": "David Wessman"
                }
            ]
        },
        {"index": {"_id": "00e2e781-7af9-4f82-b4e9-14a488a3e184"}
         },
        {
            "id": "00e2e781-7af9-4f82-b4e9-14a488a3e184",
            "imdb_rating": 6.9,
            "genre": "Music",
            "title": "Axl Rose: The Prettiest Star",
            "description": "A biography of Axl Rose.",
            "director": [
                "Angela Turner"
            ],
            "actors": [
                {
                    "id": "0cce8da2-8839-4a78-a878-45f5252588c9",
                    "name": "Gilby Clarke"
                },
                {
                    "id": "1fe46055-fceb-4714-90be-5c3a8728d020",
                    "name": "Barbara Church"
                },
                {
                    "id": "89734888-0254-4040-b87c-30e2cb144d0d",
                    "name": "Bernard Baur"
                },
                {
                    "id": "8aee78d1-87f4-4269-bb10-3d58ab009c2c",
                    "name": "Steven Adler"
                }
            ],
            "writers": [
                {
                    "id": "37c36461-9a0d-4fd9-b257-fae0b2b6e8ad",
                    "name": "Angela Turner"
                }
            ]
        }
    ]

    test_data = {
        "films_positive": [
            (
                f"Получение списка фильмов без фильтров",
                {
                    "body_el": body_el,
                    "params": {
                        "limit": 9,
                        "sort": None,
                        "genre": None,
                        "actor": None
                    }
                }
             )],
        "filter_limit": [
            (
                f"Получение списка фильмов с заданым лимитом",
                {
                    "body_el": body_el,
                    "params": {
                        "limit": 2,
                        "sort": None,
                        "genre": None,
                        "actor": None
                    }
                }
            )],
        "filter_imdb_rating": [
            (
                f"Получение списка фильмов и проверка сортировки по -imdb_rating",
                {
                    "body_el": body_el,
                    "params": {
                        "limit": 10,
                        "sort": "-imdb_rating",
                        "genre": None,
                        "actor": None
                    }
                }
            ),
            (
                f"Получение списка фильмов и проверка сортировки по imdb_rating",
                {
                    "body_el": body_el,
                    "params": {
                        "limit": 10,
                        "sort": "imdb_rating",
                        "genre": None,
                        "actor": None
                    }

                }
            )],
        "filter_genre": [
            (
                f"Получение списка фильмов и проверка сортировки по genre",
                {
                    "body_el": body_el,
                    "params": {
                        "limit": 10,
                        "sort": None,
                        "genre": "Music",
                        "actor": None
                    }

                }
            )
        ],
        "filter_person": [
            (
                f"Получение списка фильмов и проверка сортировки по genre",
                {
                    "body_el": body_el,
                    "params": {
                        "limit": 10,
                        "sort": None,
                        "genre": None,
                        "actor": "Marya Gant"
                    }

                }
            )
        ],
        "get_film_id_positive": [
            (f"Получаем информацию о фильме по его id", {'id': random.choice([item["id"] for item in body_el[1::2]])})
        ],
        "get_film_id_not_found": [
            (f"Поиск фильма по не существующему id", {'id': uuid.uuid4()})
        ]
    }
