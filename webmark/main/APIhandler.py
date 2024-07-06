from .interface import AI_Interface

class API:
    DEFAULT_REQUEST = {
        "coord_value": [],
        "text": "",
        "error": ""
    }
    DATA_INVALID = {"error": "Данные некорректны"}

    def request_update(self, data: dict):
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
            match keys_type['type']:
                case 0:
                    req['coord_value'] = AI_Interface.get_all_point(),

                case 1:
                    req['coord_value'] = AI_Interface.get_coord(keys_type),
                    req['text'] = 'Описание точки'

                
            return req
                