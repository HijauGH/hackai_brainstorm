import numpy as np
import json

class AI_Interface:
    def get_all_point():
        points = []
        
        with open('main/ai/data.json', 'r') as file:
                data = json.load(file)

        for index, item in enumerate(data):
                for point in item['points']:
                        points.append([point['lat'], point['lon']])
        
        return [
              {
                    "coord": points,
                    "value": ''
              }
        ]

    def get_coord(kwargs) -> list[dict]:
        """
        Вызов нейросети и получение от неё данных
        """
        # return позже будет заменён
        return [
                {
                        "coord": [np.random.random() for i in range(2)],
                        "value": np.random.random()
                }
                for i in range(10)
        ]