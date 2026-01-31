import { ApplicantForm } from './applicant-form.model';
import { LoanRequest } from './loan-request.model';
import { DocumentRef } from './document-ref.model';

export interface ApplicationPackage {
  case_id?: string;           // créé par le backend
  submitted_at?: string;      // créé par le backend
  applicant_form: ApplicantForm;
  loan_request: LoanRequest;
  documents: DocumentRef[];
}
