import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ApplicationService {
  private api = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  runDocumentAgent(applicationPackage: any) {
    return this.http.post(
      `${this.api}/document-agent/test`,
      applicationPackage
    );
  }
}
