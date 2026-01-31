// Service pour gérer les résultats des dossiers
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AuthService } from './auth-service';

@Injectable({
  providedIn: 'root'
})
export class OutcomeService {

  private API_URL = 'http://localhost:8000';

   constructor(
    private http: HttpClient,
    private auth: AuthService
  ) {}

  private getAuthHeaders(): HttpHeaders {
    const token = this.auth.getToken();
    return new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  }

  submitOutcome(payload: {
      case_id: string;
      outcome: string;
      loss_amount?: number;
    }): Observable<any> {
      return this.http.post(`${this.API_URL}/outcome`, payload, {
        headers: this.getAuthHeaders()
      });
    }
}