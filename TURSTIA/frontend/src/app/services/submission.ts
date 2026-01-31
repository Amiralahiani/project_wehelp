import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SubmissionService  {

  private API_URL = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  submitApplication(payload: any): Observable<any> {
    return this.http.post(`${this.API_URL}/submit-application`, payload);
  }
}
