import { Component } from '@angular/core';
import { MapService } from './services/map.service';
import { ICreatePolygon } from 'src/app/shared/types/map.types';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
})
export class MapComponent {
  constructor(public mapService: MapService) {}

  public generatePolygon() {
    const polygon: ICreatePolygon = {
      fillColor: '#00FF0088',
      hintContent: 'название района или чет такое',
      points: this.mapService.points,
    };
    this.mapService.generatePolygon(polygon);
  }
}
