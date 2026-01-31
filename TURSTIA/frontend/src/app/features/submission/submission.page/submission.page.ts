import { Component, ViewChild } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApplicationService } from '../../../services/application.service';
import { ApplicantFormComponent } from '../applicant-form.component/applicant-form.component';
import { LoanFormComponent } from '../loan-form.component/loan-form.component';
import { DocumentUploadComponent } from '../document-upload.component/document-upload.component';
import { HttpClient } from '@angular/common/http';
import { SubmissionService } from 'src/app/services/submission';
import { Router } from '@angular/router';

@Component({
  selector: 'app-submission',
  standalone: true,
  imports: [
    CommonModule,
    ApplicantFormComponent,
    LoanFormComponent,
    DocumentUploadComponent,
    ReactiveFormsModule
],
  templateUrl: './submission.page.html',
  styleUrls: ['./submission.page.css']
})
export class SubmissionPage {

  applicantForm!: FormGroup;
  loanForm!: FormGroup;
  documents: any[] = [];
  documentResult: any = null;



  constructor(
    private submissionService: SubmissionService,
    private router: Router,
    private http: HttpClient
  ) {}

  onApplicantFormChange(form: FormGroup) {
    this.applicantForm = form;
  }

  onLoanFormChange(form: FormGroup) {
    this.loanForm = form;
  }

  onDocumentsUpdate(docs: any[]) {
    this.documents = docs;
  }

  generateCaseId(prefix: string = "APP"): string {
    const today = new Date();
    const dateStr = today.toISOString().slice(0,10).replace(/-/g, ""); // YYYYMMDD

    // Récupérer le compteur depuis localStorage (ou backend si tu veux persistant)
    const key = `case_counter_${dateStr}`;
    let counter = Number(localStorage.getItem(key) || 0);
    counter += 1;
    localStorage.setItem(key, counter.toString());

    // Formater sur 4 chiffres
    const counterStr = counter.toString().padStart(4, "0");

    return `${prefix}-${dateStr}-${counterStr}`;
  }
  
  formSubmitted = false;

  onSubmit() {

    this.formSubmitted = true;

    if (!this.applicantForm || !this.loanForm) {
      console.log("⛔ Forms not ready");
      return;
    }

    if (this.applicantForm.invalid || this.loanForm.invalid) {
      console.log("⛔ Form invalid");
      return;
    }

    if (!this.documents || this.documents.length === 0) {
      console.log("⛔ No documents uploaded");
      return;
    }

    const payload = {
      case_id: this.generateCaseId("CASE"),
      applicant_form: this.applicantForm.value,
      loan_request: this.loanForm.value,

      // ✅ DOCUMENTS TRANSMIS AU BACKEND
      documents: this.documents.map((doc, index) => ({
        doc_id: doc.doc_id || `D${index + 1}`,
        type: doc.type,
        filename: doc.filename,
        content_base64: doc.content_base64
      }))
    };

    console.log("📤 Payload envoyé au backend :", payload);

    this.submissionService.submitApplication(payload).subscribe({
      next: (result) => {
        console.log("✅ Supervisor result:", result);

        this.router.navigate(
          ['/dashboard'],
          { state: { decisionResult: result } }
        );
      },
      error: (err) => {
        console.error("❌ Submission failed:", err);
      }
    });
  }
}

