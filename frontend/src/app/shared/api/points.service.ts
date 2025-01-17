import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.development';
import { HttpHeaders } from '@angular/common/http';
import { ICreatePoint } from '../types/map.types';

export const headers = new HttpHeaders({
  'Content-Type': 'application/json',
  'X-Requested-With': 'XMLHttpRequest',
  'Access-Control-Allow-Origin': '*',
});
@Injectable({ providedIn: 'root' })
export class pointsService {
  constructor(private http: HttpClient) {}

  public getAllPoints() {
    return this.http.get<any>(
      environment.apiUrl,
      { headers: headers }
    );
  }

  public getPointsBy(createData: ICreatePoint) {
    return this.http.post<any>(environment.apiUrl, createData, {
      headers: headers,
    });
  }
}
