import { Component } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { pointsService } from 'src/app/shared/api/points.service';
import { MapService } from 'src/app/widgets/map/services/map.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  constructor(
    public mapService: MapService,
    private pointsService: pointsService
  ) {
    pointsService.getAllPoints();
  }

  public form = new FormGroup({
    place: new FormControl(''),
    amount: new FormControl(''),
    gender: new FormControl(''),
    ageFrom: new FormControl(null, [Validators.min(0)]),
    ageTo: new FormControl(null, [Validators.min(0)]),
    income: new FormControl(''),
  });

  public options = [
    {
      value: 'Мужчина',
    },
    {
      value: 'Женщина',
    },
    {
      value: 'Другое',
    },
  ];
  // public setCurrency() {}
  // public removeCurrency();
}
