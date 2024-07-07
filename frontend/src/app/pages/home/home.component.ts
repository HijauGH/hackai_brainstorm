import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { catchError, of, switchMap } from 'rxjs';
import { pointsService } from 'src/app/shared/api/points.service';
import { ICreatePoint, IGetPoints } from 'src/app/shared/types/map.types';
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
  ) {}

  public dataIsLoading = false;
  public form = new FormGroup({
    adSides: new FormControl(null, [Validators.min(0), Validators.required]),
    gender: new FormControl('', [Validators.required]),
    ageFrom: new FormControl(null, [Validators.min(0), Validators.required]),
    ageTo: new FormControl(null, [Validators.min(0), Validators.required]),
    income: new FormControl('', [Validators.required]),
  });

  public genderOptions = [
    {
      text: 'Мужчина',
      value: 'male',
    },
    {
      text: 'Женщина',
      value: 'female',
    },
    {
      text: 'Все',
      value: 'all',
    },
  ];
  public formatValue(value: any) {
    return { ...value, type: 1 } as ICreatePoint;
  }

  public getPoints(value: ICreatePoint) {

    this.dataIsLoading = true;
    this.pointsService
      .getPointsBy({ ...value })
      .pipe(
        switchMap((points: IGetPoints) => 
         this.mapService.generatePoints(points, 'colored')
        ),
        catchError(error => {
          console.log(error.message);
          return of(null);
        })
      )
      .subscribe(() => {
        this.dataIsLoading = false;
      });
  }
}

