import json
import os


async def extract_json_from_file(file_name: str) -> tuple:
    path = f'tests/functional/testdata/{file_name}.json'
    if not os.path.exists(path):
        path = f'../testdata/{file_name}.json'
    with open(path) as json_file:
        data = json.load(json_file)
    return data
