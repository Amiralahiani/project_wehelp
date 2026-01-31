from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


# ========================================
# 1️⃣ MÉTADONNÉES DE L'INTERACTION
# ========================================

class ContactChannel(str, Enum):
    PHONE_CALL = "PHONE_CALL"
    EMAIL = "EMAIL"
    SMS_WHATSAPP = "SMS_WHATSAPP"
    PHYSICAL_MEETING = "PHYSICAL_MEETING"


class InteractionMetadata(BaseModel):
    interaction_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    contact_channel: ContactChannel
    duration_minutes: Optional[int] = None
    agent_responsible: Optional[str] = None


# ========================================
# 2️⃣ IDENTIFICATION DU CLIENT
# ========================================

class ClientStatus(str, Enum):
    REGULAR = "REGULAR"
    OCCASIONAL = "OCCASIONAL"
    NEW = "NEW"


class InteractionFrequency(str, Enum):
    RARE = "RARE"
    MEDIUM = "MEDIUM"
    FREQUENT = "FREQUENT"


class ClientIdentity(BaseModel):
    client_id: Optional[str] = None
    full_name: Optional[str] = Field(None, description="Masked for privacy")
    age: int
    client_status: ClientStatus
    banking_seniority_years: Optional[float] = None
    interaction_frequency: InteractionFrequency


# ========================================
# 3️⃣ SITUATION PERSONNELLE & FAMILIALE
# ========================================

class MaritalStatus(str, Enum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"


class SpouseProfessionalStatus(str, Enum):
    EMPLOYED = "EMPLOYED"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    UNEMPLOYED = "UNEMPLOYED"


class SpouseInfo(BaseModel):
    professional_status: SpouseProfessionalStatus
    monthly_income: Optional[float] = None


class PersonalSituation(BaseModel):
    marital_status: MaritalStatus
    dependents_count: int = 0
    spouse_exists: bool = False
    spouse_info: Optional[SpouseInfo] = None


# ========================================
# 4️⃣ SITUATION PROFESSIONNELLE DU CLIENT
# ========================================

class ProfessionalStatus(str, Enum):
    EMPLOYEE_CDI = "EMPLOYEE_CDI"
    EMPLOYEE_CDD = "EMPLOYEE_CDD"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    ENTREPRENEUR = "ENTREPRENEUR"
    UNEMPLOYED = "UNEMPLOYED"


class JobStability(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ProfessionalSituation(BaseModel):
    professional_status: ProfessionalStatus
    sector: Optional[str] = None
    seniority_years: Optional[float] = None
    stability: JobStability


# ========================================
# 5️⃣ SITUATION FINANCIÈRE
# ========================================

class BankingHistory(str, Enum):
    NO_INCIDENT = "NO_INCIDENT"
    MINOR_INCIDENTS = "MINOR_INCIDENTS"
    MAJOR_INCIDENTS = "MAJOR_INCIDENTS"


class FinancialSituation(BaseModel):
    monthly_income_net: float
    monthly_fixed_expenses: float
    existing_credits_total: Optional[float] = 0
    existing_credits_monthly_payment: Optional[float] = 0
    debt_ratio: Optional[float] = None  # Will be calculated if not provided
    available_savings: Optional[float] = None
    banking_history: BankingHistory


# ========================================
# 6️⃣ DEMANDE DE CRÉDIT
# ========================================

class CreditType(str, Enum):
    REAL_ESTATE = "REAL_ESTATE"
    PERSONAL = "PERSONAL"
    AUTO = "AUTO"
    PROFESSIONAL = "PROFESSIONAL"


class CreditPurpose(str, Enum):
    INVESTMENT = "INVESTMENT"
    NECESSARY_EXPENSE = "NECESSARY_EXPENSE"
    COMFORT_EXPENSE = "COMFORT_EXPENSE"


class CreditRequest(BaseModel):
    credit_type: CreditType
    amount_requested: float
    duration_months: int
    estimated_monthly_payment: Optional[float] = None
    purpose: CreditPurpose


# ========================================
# 7️⃣ INDICATEURS COMPORTEMENTAUX
# ========================================

class StressLevel(int, Enum):
    VERY_CALM = 1
    CALM = 2
    NEUTRAL = 3
    STRESSED = 4
    VERY_STRESSED = 5


class UrgencyLevel(int, Enum):
    NOT_URGENT = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    EXTREMELY_URGENT = 5


class ProjectClarity(int, Enum):
    VERY_VAGUE = 1
    VAGUE = 2
    SOMEWHAT_CLEAR = 3
    CLEAR = 4
    VERY_STRUCTURED = 5


class EngagementLevel(int, Enum):
    WEAK = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


class CoherenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class BehavioralIndicators(BaseModel):
    stress_level: StressLevel
    urgency_level: UrgencyLevel
    project_clarity: ProjectClarity
    engagement_level: EngagementLevel
    discourse_coherence: CoherenceLevel


# ========================================
# 8️⃣ INTENTION RÉELLE DU CLIENT
# ========================================

class MainMotivation(str, Enum):
    NECESSITY = "NECESSITY"
    OPPORTUNITY = "OPPORTUNITY"
    EXTERNAL_PRESSURE = "EXTERNAL_PRESSURE"


class ProjectionCapacity(str, Enum):
    SHORT_TERM_ONLY = "SHORT_TERM_ONLY"
    MEDIUM_TERM = "MEDIUM_TERM"
    LONG_TERM = "LONG_TERM"


class RealIntention(BaseModel):
    main_motivation: MainMotivation
    projection_capacity: ProjectionCapacity


# ========================================
# 9️⃣ RISQUES IDENTIFIÉS
# ========================================

class RiskChecklist(BaseModel):
    professional_instability: bool = False
    high_debt: bool = False
    spouse_income_dependency: bool = False
    non_priority_project: bool = False
    excessive_urgency: bool = False
    incoherent_discourse: bool = False


# ========================================
# 🔟 SYNTHÈSE STRUCTURÉE – IA READY
# ========================================

class GlobalRiskProfile(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TheoreticalRepaymentCapacity(str, Enum):
    INSUFFICIENT = "INSUFFICIENT"
    ACCEPTABLE = "ACCEPTABLE"
    SOLID = "SOLID"


class Synthesis(BaseModel):
    global_risk_profile: GlobalRiskProfile
    theoretical_repayment_capacity: TheoreticalRepaymentCapacity


# ========================================
# MAIN: EXPANDED APPLICATION PACKAGE
# ========================================

class DocumentRef(BaseModel):
    """Existing document reference model - kept for compatibility"""
    doc_id: str
    type: str  # ID_CARD | BANK_STATEMENT | CONTRACT
    uri: str


class ExpandedApplicationPackage(BaseModel):
    """
    Unified form that contains ALL data needed for:
    - ML Risk Model (structured fields)
    - Qdrant/RAG Pipeline (will be converted to text summary)
    """
    case_id: Optional[str] = Field(None, description="Generated by backend")
    submitted_at: Optional[datetime] = Field(None, description="Submission timestamp")

    # === FORM SECTIONS ===
    interaction_metadata: InteractionMetadata
    client_identity: ClientIdentity
    personal_situation: PersonalSituation
    professional_situation: ProfessionalSituation
    financial_situation: FinancialSituation
    credit_request: CreditRequest
    behavioral_indicators: BehavioralIndicators
    real_intention: RealIntention
    risk_checklist: RiskChecklist
    synthesis: Synthesis

    # === DOCUMENTS (for Qdrant pipeline) ===
    documents: List[DocumentRef] = []
