import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class FraudService {

  private api = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getFraudStatus(caseId: string) {
    return this.http.get<any>(`${this.api}/fraud_status/${caseId}`);
  }

  getAuditTimeline(caseId: string) {
    return this.http.get<any>(`${this.api}/audit_timeline/${caseId}`);
  }
}