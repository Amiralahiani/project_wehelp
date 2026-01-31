// frontend/src/app/core/models/expanded-application.model.ts

export interface InteractionMetadata {
    interaction_id?: string;
    timestamp?: string;
    contact_channel: 'PHONE_CALL' | 'EMAIL' | 'SMS_WHATSAPP' | 'PHYSICAL_MEETING';
    duration_minutes?: number;
    agent_responsible?: string;
}

export interface ClientIdentity {
    client_id?: string;
    full_name?: string;
    age: number;
    client_status: 'REGULAR' | 'OCCASIONAL' | 'NEW';
    banking_seniority_years?: number;
    interaction_frequency: 'RARE' | 'MEDIUM' | 'FREQUENT';
}

export interface SpouseInfo {
    professional_status: 'EMPLOYED' | 'SELF_EMPLOYED' | 'UNEMPLOYED';
    monthly_income?: number;
}

export interface PersonalSituation {
    marital_status: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED';
    dependents_count: number;
    spouse_exists: boolean;
    spouse_info?: SpouseInfo;
}

export interface ProfessionalSituation {
    professional_status: 'EMPLOYEE_CDI' | 'EMPLOYEE_CDD' | 'SELF_EMPLOYED' | 'ENTREPRENEUR' | 'UNEMPLOYED';
    sector?: string;
    seniority_years?: number;
    stability: 'LOW' | 'MEDIUM' | 'HIGH';
}

export interface FinancialSituation {
    monthly_income_net: number;
    monthly_fixed_expenses: number;
    existing_credits_total?: number;
    existing_credits_monthly_payment?: number;
    debt_ratio?: number;
    available_savings?: number;
    banking_history: 'NO_INCIDENT' | 'MINOR_INCIDENTS' | 'MAJOR_INCIDENTS';
}

export interface CreditRequest {
    credit_type: 'REAL_ESTATE' | 'PERSONAL' | 'AUTO' | 'PROFESSIONAL';
    amount_requested: number;
    duration_months: number;
    estimated_monthly_payment?: number;
    purpose: 'INVESTMENT' | 'NECESSARY_EXPENSE' | 'COMFORT_EXPENSE';
}

export interface BehavioralIndicators {
    stress_level: 1 | 2 | 3 | 4 | 5;
    urgency_level: 1 | 2 | 3 | 4 | 5;
    project_clarity: 1 | 2 | 3 | 4 | 5;
    engagement_level: 1 | 2 | 3 | 4 | 5;
    discourse_coherence: 'LOW' | 'MEDIUM' | 'HIGH';
}

export interface RealIntention {
    main_motivation: 'NECESSITY' | 'OPPORTUNITY' | 'EXTERNAL_PRESSURE';
    projection_capacity: 'SHORT_TERM_ONLY' | 'MEDIUM_TERM' | 'LONG_TERM';
}

export interface RiskChecklist {
    professional_instability: boolean;
    high_debt: boolean;
    spouse_income_dependency: boolean;
    non_priority_project: boolean;
    excessive_urgency: boolean;
    incoherent_discourse: boolean;
}

export interface Synthesis {
    global_risk_profile: 'LOW' | 'MEDIUM' | 'HIGH';
    theoretical_repayment_capacity: 'INSUFFICIENT' | 'ACCEPTABLE' | 'SOLID';
}

export interface DocumentRef {
    doc_id: string;
    type: string;
    uri: string;
    content?: string; // Base64
}

export interface ExpandedApplicationPackage {
    case_id?: string;
    submitted_at?: string;
    interaction_metadata: InteractionMetadata;
    client_identity: ClientIdentity;
    personal_situation: PersonalSituation;
    professional_situation: ProfessionalSituation;
    financial_situation: FinancialSituation;
    credit_request: CreditRequest;
    behavioral_indicators: BehavioralIndicators;
    real_intention: RealIntention;
    risk_checklist: RiskChecklist;
    synthesis: Synthesis;
    documents: DocumentRef[];
}
