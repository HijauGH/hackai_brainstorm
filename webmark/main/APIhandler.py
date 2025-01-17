from .interface import *

class API:
    DEFAULT_REQUEST = {
        "coord_value": [],
        "text": "",
        "error": ""
    }
    DATA_INVALID = {"error": "Данные некорректны"}

    def get_point_request(self, data):
        print(data)
        req, keys_type = self.request(data)
        coord, value = AI_Interface.get_coord(keys_type)
        req['coord_value'] = [{'coord': coord, 'value': value}]
        req['text'] = f'Было найдено {len(coord)} точек. Они принесут ~{value} охвата'

        return req

    def get_all_point_request(self):
        req = self.DEFAULT_REQUEST.copy()
        req['coord_value'] = AI_Interface.get_all_point()

        return req

    def request(self, data: dict):
        keys_type = {
            "adSides": 0,
            "gender": '',
            "ageFrom": 0,
            "ageTo": 0,
            "income": '',
            'type': 0
        }

        # Проверка типов данных
        for key in keys_type.keys():
            try:
                _ = type(keys_type[key])(data[key])

            except ValueError:
                return self.DATA_INVALID

            else:
                keys_type[key] = _

        else:
            req = self.DEFAULT_REQUEST.copy()
            return req, keys_type