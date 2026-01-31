from pydantic import BaseModel
from typing import List, Optional

class ConsistencyCheck(BaseModel):
    check: str
    status: str
    declared: Optional[float] = None
    detected: Optional[float] = None
    delta: Optional[float] = None
    score: Optional[float] = None
    months: Optional[int] = None

class FinalProfile(BaseModel):
    age: Optional[int] = 0
    employment_type: Optional[str] = None
    sector: Optional[str] = None
    monthly_income: Optional[float] = 0.0
    monthly_expenses: Optional[float] = 0.0
    debt_ratio: Optional[float] = 0.0
    income_expense_ratio: Optional[float] = 0.0
    late_payments: Optional[int] = 0
    other_loans_count: Optional[int] = 0
    contract_duration_months: Optional[int] = 0
    stability_score: Optional[float] = 0.0

class ProfileFusionResult(BaseModel):
    case_id: str
    final_profile: FinalProfile
    consistency_checks: List[ConsistencyCheck]
    profile_confidence: float
    missing_data: List[str]