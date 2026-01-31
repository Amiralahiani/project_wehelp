# Data Contracts — Credit Decision Memory System

This document defines the **official input and output schemas**.
These schemas are **frozen** after validation.

---

## Input Contract — ApplicationPackage

This object represents a credit application submitted to the system.

### Root fields
- case_id: string (unique identifier)
- submitted_at: ISO 8601 datetime string

---

### applicant_form
Declarative information provided by the applicant.

- age: number
- employment_type: string
- monthly_income_declared: number
- monthly_expenses_declared: number
- sector: string
- late_payments_declared: number

---

### loan_request
Details of the requested credit product.

- loan_amount: number
- term_months: number
- product: string
- purpose: string

---

### documents (optional)
Uploaded supporting documents.

- doc_id: string
- type: ID_CARD | BANK_STATEMENT | CONTRACT
- uri: string

---

## Output Contract — CaseDecisionResponse

Returned by the system after evaluation.

### Common fields (all modes)
- case_id: string
- mode: NORMAL | FRAUD_STOP | COLD_START
- top_similarity: number
- confidence: number
- audit_id: string

---

### Mode: NORMAL
Decision produced using similar historical cases.

- decision: ACCEPT | REJECT | ACCEPT_WITH_GUARANTEE
- scenarios: array
- similar_cases: array
- explanation: string

---

### Mode: FRAUD_STOP
Fraud detected. Credit workflow is suspended.

- fraud_risk_level: HIGH
- fraud_reasons: array
- similar_fraud_cases: array

---

### Mode: COLD_START
No sufficiently similar cases found.

- ai_recommendation: ACCEPT | ACCEPT_WITH_GUARANTEE | REJECT
- human_validation_required: true
- reason: string

---

## Scenario Object

Used in NORMAL and COLD_START modes.

- scenario: ACCEPT | REJECT | ACCEPT_WITH_GUARANTEE
- similar_cases: number
- default_rate: number
- expected_outcome: string

---

## SimilarCase Object

Represents a retrieved historical case from Qdrant.

- case_id: string
- similarity: number
- decision: string
- outcome: REPAID | DEFAULT
