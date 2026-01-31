// frontend/src/app/features/submission/expanded-submission/expanded-submission.component.ts

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ExpandedApplicationPackage } from '../../../core/models/expanded-application.model';

@Component({
    selector: 'app-expanded-submission',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './expanded-submission.component.html',
    styleUrls: ['./expanded-submission.component.css']
})
export class ExpandedSubmissionComponent {

    formData: Partial<ExpandedApplicationPackage> = {
        interaction_metadata: {
            contact_channel: 'PHONE_CALL',
            duration_minutes: undefined,
            agent_responsible: ''
        },
        client_identity: {
            age: 0,
            client_status: 'NEW',
            interaction_frequency: 'RARE',
            banking_seniority_years: undefined
        },
        personal_situation: {
            marital_status: 'SINGLE',
            dependents_count: 0,
            spouse_exists: false
        },
        professional_situation: {
            professional_status: 'EMPLOYEE_CDI',
            sector: '',
            seniority_years: undefined,
            stability: 'MEDIUM'
        },
        financial_situation: {
            monthly_income_net: 0,
            monthly_fixed_expenses: 0,
            existing_credits_total: 0,
            existing_credits_monthly_payment: 0,
            available_savings: 0,
            banking_history: 'NO_INCIDENT'
        },
        credit_request: {
            credit_type: 'PERSONAL',
            amount_requested: 0,
            duration_months: 12,
            purpose: 'NECESSARY_EXPENSE'
        },
        behavioral_indicators: {
            stress_level: 3,
            urgency_level: 3,
            project_clarity: 3,
            engagement_level: 3,
            discourse_coherence: 'MEDIUM'
        },
        real_intention: {
            main_motivation: 'NECESSITY',
            projection_capacity: 'MEDIUM_TERM'
        },
        risk_checklist: {
            professional_instability: false,
            high_debt: false,
            spouse_income_dependency: false,
            non_priority_project: false,
            excessive_urgency: false,
            incoherent_discourse: false
        },
        synthesis: {
            global_risk_profile: 'MEDIUM',
            theoretical_repayment_capacity: 'ACCEPTABLE'
        },
        documents: []
    };

    submitting = false;
    result: any = null;
    error: string | null = null;

    constructor(private http: HttpClient) { }

    onSpouseExistsChange() {
        if (this.formData.personal_situation!.spouse_exists) {
            this.formData.personal_situation!.spouse_info = {
                professional_status: 'EMPLOYED',
                monthly_income: undefined
            };
        } else {
            this.formData.personal_situation!.spouse_info = undefined;
        }
    }

    calculateDebtRatio() {
        const income = this.formData.financial_situation!.monthly_income_net;
        const debt = this.formData.financial_situation!.existing_credits_monthly_payment || 0;
        if (income > 0) {
            this.formData.financial_situation!.debt_ratio = debt / income;
        }
    }

    onSubmit() {
        this.submitting = true;
        this.error = null;
        this.result = null;

        // Calculate debt ratio before submission
        this.calculateDebtRatio();

        // Generate case_id and timestamp
        const timestamp = new Date().toISOString();
        const caseId = `CASE-${Date.now()}`;

        const submission: ExpandedApplicationPackage = {
            ...this.formData as ExpandedApplicationPackage,
            case_id: caseId,
            submitted_at: timestamp
        };

        console.log('📋 Submitting extended application:', submission);

        this.http.post('http://localhost:8000/api/submit-extended', submission)
            .subscribe({
                next: (response: any) => {
                    console.log('✅ Submission successful:', response);
                    this.result = response;
                    this.submitting = false;
                },
                error: (error) => {
                    console.error('❌ Submission failed:', error);
                    this.error = error.error?.detail || 'Submission failed. Please try again.';
                    this.submitting = false;
                }
            });
    }

    resetForm() {
        window.location.reload();
    }
}
