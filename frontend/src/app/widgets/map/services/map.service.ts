/* eslint-disable @typescript-eslint/no-explicit-any */
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {
  ICreatePolygon,
  IGetPoints,
  Point,
} from 'src/app/shared/types/map.types';
import { Observable, of } from 'rxjs';
import { pointsService } from 'src/app/shared/api/points.service';

declare let ymaps: any;

@Injectable()
export class MapService {
  constructor(
    private http: HttpClient,
    private pointsService: pointsService
  ) {
    ymaps.ready(this.initMap.bind(this));
  }
  public yandexMap: any;
  public points: Point[] = [];
  public pointsInPolygons: Point[] = [];
  public polygons: any[] = [];
  public text = '';

  private initMap() {
    this.createMap();

    // this.pointsService.getAllPoints().subscribe(p =>
    //   this.generatePoints(
    //     {
    //       coord_value: [{ coord: [55.76, 37.64], value: 23 }],
    //       text: '',
    //       error: '',
    //     },
    //     '#00000'
    //   )
    // );

    this.yandexMap.events.add('click', (e: any) => this.clickFn(e));
  }

  private createMap() {
    this.yandexMap = new ymaps.Map('map', {
      center: [37.64, 55.76],
      zoom: 10,
    });

    this.generatePoints(
      {
        coord_value: [{ coord: [37.64, 55.76], value: 23 }],
        text: '',
        error: '',
      },
      'default'
    );
  }

  private clickFn(e: any) {
    const coords = e.get('coords');

    const placemark = new ymaps.Placemark(
      coords,
      {
        // custom: [
        //   {
        //     name: 'qwe',
        //   },
        //   {
        //     age: 5,
        //   },
        // ],
      },
      {
        draggable: true,
      }
    );
    // placemark.events.add('click', () => {
    //   console.log(placemark.properties);

    //   console.log(placemark.properties.get('custom'));
    // });

    this.yandexMap.geoObjects.add(placemark);

    this.points.push(coords);

    placemark.events.add('dragend', (e: any) => this.dragFn(e, coords));
  }

  private dragFn(e: any, coords: any) {
    const newCoords = e.get('target').geometry.getCoordinates();

    const index = this.points.indexOf(coords);
    if (index !== -1) {
      this.points[index] = newCoords;
    }
    coords = newCoords;
  }

  public generatePoints(points: IGetPoints, colorType: 'default' | 'colored') {
    this.yandexMap.geoObjects.removeAll();
    points.coord_value.forEach(el => {
      const placemark = new ymaps.Placemark(
        el.coord,
        {},
        {
          draggable: true,
          iconLayout: 'default#image',
          iconImageHref:
            colorType === 'default'
              ? 'assets/img/icons/marker.svg'
              : 'assets/img/icons/marker-red.svg',
        }
      );
      this.yandexMap.geoObjects.add(placemark);
    });

    return of();
  }

  public generatePolygon(polygon: ICreatePolygon) {
    const myPolygon = new ymaps.Polygon(
      [
        // Указываем координаты вершин многоугольника.
        // Координаты вершин внешнего контура.
        polygon.points,
      ],
      {
        // Описываем свойства геообъекта.
        // Содержимое балуна.
        hintContent: polygon.hintContent,
      },
      {
        // Задаем опции геообъекта.
        // Цвет заливки.
        fillColor: polygon.fillColor,
        opacity: 0.5,
        // Ширина обводки.
        strokeWidth: 5,
      }
    );
    this.polygons.push(myPolygon);
    // Добавляем многоугольник на карту.
    this.yandexMap.geoObjects.add(myPolygon);
    myPolygon.events.add('click', (e: any) => this.clickFn(e));
  }

  public getPointsInPolygons(polygons: any) {
    const res: any[] = [];
    polygons.forEach((polygon: any) => {
      console.log(polygon);

      const pointsInPolygon = this.points.filter(
        //TODO:pointIsVertex кривой
        (point: Point) =>
          polygon.geometry.contains(point) &&
          !this.pointIsVertex(polygon, point)
      );
      res.push({
        name: polygon.properties.get('hintContent'),
        points: pointsInPolygon,
      });
    });
    console.log(res);
  }
  private pointIsVertex(polygon: any, point: Point) {
    return polygon.geometry
      .getCoordinates()
      .some((points: Point[]) =>
        points.some((p: Point) => this.isSamePoint(p, point))
      );
  }
  private isSamePoint(pointA: Point, pointB: Point) {
    return pointA[0] === pointB[0] && pointA[1] === pointB[1];
  }

  // private getCityBoundaries(cityName: string): Observable<any> {
  //   const url = 'http://nominatim.openstreetmap.org/search';
  //   const params = {
  //     q: cityName,
  //     format: 'json',
  //     polygon_geojson: '1',
  //   };
  //   return this.http.get(url, { params });
  // }

  // public findPlace(placeName: string): void {
  //   this.getCityBoundaries(placeName).subscribe(
  //     (data: any) => {
  //       if (data.length > 0) {
  //         console.log(data);

  //         data.forEach((place: any) => {
  //           if (place.osm_type === 'relation') {
  //             const coordinates = place.geojson.coordinates;
  //             const cityPolygon = new ymaps.GeoObject(
  //               {
  //                 geometry: {
  //                   type: 'Polygon',
  //                   coordinates: coordinates,
  //                 },
  //               },
  //               {
  //                 fillColor: '#00FF0088', // Цвет заливки
  //                 strokeColor: '#0000FF', // Цвет обводки
  //                 strokeWidth: 2, // Ширина обводки
  //               }
  //             );

  //             // Удаляем предыдущий полигон, если он был
  //             this.yandexMap.geoObjects.removeAll();

  //             // Добавляем новый полигон на карту
  //             this.yandexMap.geoObjects.add(cityPolygon);

  //             // Устанавливаем центр карты на координаты города
  //             const bounds = cityPolygon.geometry.getBounds();
  //             this.yandexMap.setBounds(bounds, { checkZoomRange: true });
  //           }
  //         });
  //       } else {
  //         alert('Границы города не найдены');
  //       }
  //     },
  //     (error: any) => {
  //       console.error('Error fetching city boundaries:', error);
  //       alert('Ошибка при получении границ города');
  //     }
  //   );
  // }
}
