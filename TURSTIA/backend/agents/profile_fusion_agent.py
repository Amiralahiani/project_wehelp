from typing import Dict, Any 
from ..schemas.profile_fusion import ( ProfileFusionResult, FinalProfile, ConsistencyCheck )

def check_field(name, declared, detected, tolerance=0):
    """Crée un consistency check générique"""
    if declared is None and detected is None:
        return "MISSING", None
    if declared is None or detected is None:
        return "PARTIAL", None
    delta = abs(declared - detected) if isinstance(declared, (int, float)) else 0
    status = "WARN" if delta > tolerance else "OK"
    return status, delta


def weighted_average(declared: float, detected: float, w_declared: float = 0.5, w_detected: float = 0.5) -> float: 
    return (declared * w_declared + detected * w_detected) / (w_declared + w_detected)

def compute_ratios(income: float, expenses: float, debt: float) -> Dict[str, float]: 
    debt_ratio = debt / income if income > 0 else 0 
    income_expense_ratio = income / expenses if expenses > 0 else 0 
    return { 
        "debt_ratio": round(debt_ratio, 2), 
        "income_expense_ratio": round(income_expense_ratio, 2) 
    }

def stability_score(contract_months: int, late_payments: int, other_loans: int) -> float: 
    contract_months = contract_months or 0 
    late_payments = late_payments or 0 
    other_loans = other_loans or 0

    score = 0.0 
    score += min(contract_months / 24, 1.0) * 0.28
    score += (1 - min(late_payments / 5, 1.0)) * 0.32
    score += (1 - min(other_loans / 5, 1.0)) * 0.28
    return round(score, 2)

def compute_profile_confidence(missing_data, checks, stability_score,delta,seuil_max): 
    confidence = 1.0
    
    # pénalité données manquantes
    confidence -= 0.1 * len(missing_data) 
    
    # pénalité WARN 
    warn_count = sum(1 for c in checks if c.status == "WARN")
    confidence -= 0.05 * warn_count 
    # pénalité mismatch revenu
    confidence -= min(delta / seuil_max, 0.2)

    # pondération avec stabilité 
    confidence = confidence * (0.7 + stability_score * 0.3) 
    
    return round(max(confidence, 0), 2)

def build_final_profile(case_id, applicant_form, loan_request, doc_signals):

    missing_data = []
    checks = []

    # ================= INCOME =================
    declared_income = applicant_form.get("monthly_income_declared")
    detected_income = doc_signals.get("detected_income")

    status, delta = check_field("income", declared_income, detected_income, tolerance=50)
    if declared_income is None: missing_data.append("monthly_income_declared")
    if detected_income is None: missing_data.append("detected_income")

    checks.append(ConsistencyCheck(
        check="income",
        status=status,
        declared=declared_income,
        detected=detected_income,
        delta=delta
    ))

    monthly_income = weighted_average(declared_income or 0, detected_income or 0)

    # ================= EXPENSES =================
    declared_expenses = applicant_form.get("monthly_expenses_declared")
    detected_expenses = doc_signals.get("detected_expenses")

    status, delta = check_field("expenses", declared_expenses, detected_expenses, tolerance=50)
    if declared_expenses is None: missing_data.append("monthly_expenses_declared")
    if detected_expenses is None: missing_data.append("detected_expenses")

    checks.append(ConsistencyCheck(
        check="expenses",
        status=status,
        declared=declared_expenses,
        detected=detected_expenses,
        delta=delta
    ))

    monthly_expenses = weighted_average(declared_expenses or 0, detected_expenses or 0)

    # ================= LOAN TERM =================
    declared_term = loan_request.get("term_months")
    detected_term = doc_signals.get("contract_duration_months")

    status, delta = check_field("loan_term", declared_term, detected_term, tolerance=3)
    if declared_term is None: missing_data.append("term_months")
    if detected_term is None: missing_data.append("contract_duration_months")

    checks.append(ConsistencyCheck(
        check="loan_term",
        status=status,
        declared=declared_term,
        detected=detected_term,
        delta=delta,
        months=detected_term or declared_term
    ))

    contract_months = detected_term or declared_term or 0

    # ================= ID =================
    declared_id = applicant_form.get("cin")
    detected_id = doc_signals.get("cin")

    if not declared_id: missing_data.append("cin_declared")
    if not detected_id: missing_data.append("cin_detected")

    status = "OK" if declared_id and detected_id and declared_id == detected_id else "WARN" if declared_id and detected_id else "MISSING"

    checks.append(ConsistencyCheck(
        check="id_match",
        status=status,
        declared=declared_id,
        detected=detected_id,
        score=1.0 if status == "OK" else 0.0 if status == "WARN" else None
    ))

    # ================= EMPLOYMENT TYPE =================
    employment_type = applicant_form.get("employment_type")
    if not employment_type:
        missing_data.append("employment_type")

    checks.append(ConsistencyCheck(
        check="employment_type",
        status="OK" if employment_type else "MISSING"
    ))

    # ================= SECTOR =================
    sector = applicant_form.get("sector")
    if not sector:
        missing_data.append("sector")

    checks.append(ConsistencyCheck(
        check="sector",
        status="OK" if sector else "MISSING"
    ))

    # ================= LATE PAYMENTS =================
    late_payments = applicant_form.get("late_payments_declared")
    if late_payments is None:
        missing_data.append("late_payments_declared")

    checks.append(ConsistencyCheck(
        check="late_payments",
        status="OK" if late_payments is not None else "MISSING",
        declared=late_payments
    ))

    # ================= RATIOS =================
    debt = loan_request.get("monthly_debt", 0)
    ratios = compute_ratios(monthly_income, monthly_expenses, debt)

    # ================= STABILITY =================
    other_loans = loan_request.get("other_loans", 0)
    stab_score = stability_score(contract_months, late_payments or 0, other_loans)

    # ================= CONFIDENCE =================
    delta_income = abs((declared_income or 0) - (detected_income or 0))
    profile_confidence = compute_profile_confidence(missing_data, checks, stab_score, delta_income, 1000)

    # ================= FINAL PROFILE =================
    final_profile = FinalProfile(
        age=applicant_form.get("age"),
        employment_type=employment_type,
        sector=sector,
        monthly_income=round(monthly_income, 2),
        monthly_expenses=round(monthly_expenses, 2),
        debt_ratio=ratios["debt_ratio"],
        income_expense_ratio=ratios["income_expense_ratio"],
        late_payments=late_payments or 0,
        other_loans_count=other_loans,
        contract_duration_months=contract_months,
        stability_score=stab_score
    )

    return ProfileFusionResult(
        case_id=case_id,
        final_profile=final_profile,
        consistency_checks=checks,
        profile_confidence=profile_confidence,
        missing_data=list(set(missing_data))
    )
