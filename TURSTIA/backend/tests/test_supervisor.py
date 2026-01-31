
from backend.agents.supervisor_agent import SupervisorAgent

supervisor = SupervisorAgent()

# =====================================================
# ❄️ CAS 1 — COLD START
# (profil atypique / éloigné de l’historique)
# =====================================================
cold_start_case = {
    "case_id": "SIM-COLD-001",
    "applicant_form": {
        "age": 19,
        "employment_type": "Student",
        "monthly_income_declared": 200,
        "monthly_expenses_declared": 180,
        "late_payments_declared": 0,
        "sector": "Other",
        "cin": "11111111"
    },
    "loan_request": {
        "loan_amount": 2000,
        "term_months": 12,
        "product": "Micro Loan",
        "monthly_debt": 0,
        "other_loans": 0
    },
    "documents": []
}


# =====================================================
# 🔴 CAS 2 — FRAUDE
# (profil qui ressemble fortement aux fraudes stockées)
# =====================================================
fraud_case = {
    "case_id": "SIM-FRAUD-001",
    "applicant_form": {
        "employment_type": "Freelance",
        "sector": "Services",
        "age": 41
    },
    "loan_request": {
        "loan_amount": 30000,
        "term_months": 60,
        "default_probability": 0.42,
        "fraud_label": True
    },
    "documents": []
}

# =====================================================
# 🟢 CAS 3 — NORMAL
# (profil classique, proche de l’historique sain)
# =====================================================
normal_case = {
    "case_id": "TEST-001",
    "applicant_form": {
        "age": 26,
        "employment_type": "Freelance",
        "monthly_income_declared": 900,
        "monthly_expenses_declared": 650,
        "late_payments_declared": 1,
        "sector": "Digital Services",
        "cin": "12345678"
    },
    "loan_request": {
        "loan_amount": 10000,
        "term_months": 36,
        "product": "Personal Loan",
        "monthly_debt": 300,
        "other_loans": 1
    },
    "documents": [] 
}


# =====================================================
# 🧪 LANCEMENT DES TESTS
# =====================================================
def run_test(label, payload):
    print(f"\n==============================")
    print(f"🧪 TEST {label}")
    print(f"==============================")
    result = supervisor.run(payload)
    print(result)

if __name__ == "__main__":
    run_test("COLD START", cold_start_case)
    run_test("FRAUD", fraud_case)
    run_test("NORMAL", normal_case)


