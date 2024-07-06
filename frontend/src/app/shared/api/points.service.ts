import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.development';

@Injectable({ providedIn: 'root' })
export class pointsService {
  constructor(private http: HttpClient) {}

  public getAllPoints() {
    return this.http.get<any>(environment.apiUrl).subscribe(d => {
      console.log(d);
    });
  }
}
