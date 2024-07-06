import json

from .const import ALL_POINT
# DEV
import numpy as np


class AI:
        """
        Класс для методотов ИИ
        """
        def ping(self) -> dict:
            #FIXME
            # Вызов нейросети
            # Заменить RETURN на метод вызова нейросети
            return {"points": [{"lat": "55.573691", "lon": "37.631423", "azimuth": 273}, {"lat": "55.584765", "lon": "37.712454", "azimuth": 232}, {"lat": "55.808425457052", "lon": "37.388807961811", "azimuth": 188}, {"lat": "55.674378", "lon": "37.422364", "azimuth": 333}, {"lat": "55.608396", "lon": "37.766383", "azimuth": 54}, {"lat": "55.908622", "lon": "37.553523", "azimuth": 260}, {"lat": "55.71", "lon": "37.3875", "azimuth": 162}, {"lat": "55.626667", "lon": "37.472993", "azimuth": 327}, {"lat": "55.82762", "lon": "37.832285", "azimuth": 140}, {"lat": "55.864929", "lon": "37.402182", "azimuth": 31}, {"lat": "55.79614", "lon": "37.377824", "azimuth": 12}, {"lat": "55.878467", "lon": "37.734767", "azimuth": 135}, {"lat": "55.835535", "lon": "37.816508", "azimuth": 316}, {"lat": "55.572631", "lon": "37.648526", "azimuth": 98}, {"lat": "55.897735", "lon": "37.642363", "azimuth": 102}, {"lat": "55.668107", "lon": "37.838745", "azimuth": 346}, {"lat": "55.676858", "lon": "37.835067", "azimuth": 170}, {"lat": "55.582222", "lon": "37.706667", "azimuth": 58}, {"lat": "55.757820462245", "lon": "37.842863202095", "azimuth": 181}, {"lat": "55.877894", "lon": "37.431545", "azimuth": 66}, {"lat": "55.893822", "lon": "37.499453", "azimuth": 61}, {"lat": "55.620483", "lon": "37.788833", "azimuth": 248}, {"lat": "55.902938", "lon": "37.615667", "azimuth": 295}, {"lat": "55.775140433481", "lon": "37.370069487102", "azimuth": 179}, {"lat": "55.822007600938", "lon": "37.393082487103", "azimuth": 174}], "value": 23.51} 

        def get(self) -> dict:
            ai_data = self.ping()
            return [[point['lat'], point['lon']] for point in ai_data.get('points')], ai_data.get('value')

class AI_Interface:
    """
    Переходник для ИИ и веб-сервера
    """

    def get_all_point() -> list[dict]:
        return [{
            "coord": ALL_POINT,
            "value": 0
        }]

    def get_coord(kwargs) -> list[dict]:
        ai = AI()
        coord, value = ai.get()
        # return позже будет заменён
        return [
                {
                        "coord": coord,
                        "value": value
                }
                for i in range(10)
        ]