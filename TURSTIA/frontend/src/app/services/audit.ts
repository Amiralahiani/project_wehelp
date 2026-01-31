import { HttpClient, HttpHeaders  } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthService } from './auth-service';

@Injectable({
  providedIn: 'root',
})
export class AuditService {
  private baseUrl = 'http://localhost:8000';

  constructor(
    private http: HttpClient,
    private auth: AuthService
  ) {}

  
  private getAuthHeaders(): HttpHeaders {
    const token = this.auth.getToken();
    console.log(this.auth.getToken());
    return new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  }

  // Tous les audits
  getAllAudits(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/audit`, {
      headers: this.getAuthHeaders()
    });
  }

  // Audits par case
  getAuditByCase(caseId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/audit?case_id=${caseId}`, {
      headers: this.getAuthHeaders()
    });
  }
}
