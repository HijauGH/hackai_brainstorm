import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.development';
import { HttpHeaders } from '@angular/common/http';
export const headers = new HttpHeaders({
	'Content-Type': 'application/json',
});
@Injectable({ providedIn: 'root' })
export class pointsService {
  constructor(private http: HttpClient) {}

  public getAllPoints() {
    return this.http.post<any>(environment.apiUrl,{
			"adSides": 0,
			"gender": "male",
			"ageFrom": 0,
			"ageTo": 0,
			"income": "0",
			"type": 0
	},{headers:headers}).subscribe(d => {
      console.log(d);
    });
  }
}
