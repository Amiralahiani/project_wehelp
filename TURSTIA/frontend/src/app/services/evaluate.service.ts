// src/app/services/evaluate.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Définir le type pour le profil du client
export interface ClientProfile {
  monthly_income: number;
  monthly_expenses: number;
  debt_ratio: number;
  job_stability: number;
  top_similarity: number;
}

// Définir le type pour la réponse de l'API
export interface EvaluationResult {
  risk: any;
  scenario: any;
  decision: any;
}

@Injectable({
  providedIn: 'root'
})
export class EvaluateService {

  private apiUrl = 'http://127.0.0.1:8000/evaluate'; // ton endpoint FastAPI

  constructor(private http: HttpClient) {}

  evaluateClient(profile: ClientProfile): Observable<EvaluationResult> {
    return this.http.post<EvaluationResult>(this.apiUrl, profile);
  }
}
