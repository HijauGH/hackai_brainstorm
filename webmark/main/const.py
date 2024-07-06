from json import load as load_json

PATH_ALL_POINT: str = "main/ai/data/all_point.json"
PATH_DATA: str = "main/ai/data/data.json"
ALL_POINT: list = load_json(open(PATH_ALL_POINT, 'r', encoding='UTF-8'))
