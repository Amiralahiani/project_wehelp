import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EvaluationService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  evaluate(payload: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/evaluate`, payload);
  }

  sendFeedback(feedback: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/feedback`, feedback);
  }

  getAudit(caseId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/audit/${caseId}`);
  }
}