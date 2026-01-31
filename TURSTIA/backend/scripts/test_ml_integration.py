"""
Test ML Model Integration
Verifies that the trained model loads correctly and can make predictions
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from agents.ml_risk_agent import MLRiskAgent

# Test application data
test_application = {
    "client_identity": {
        "age": 35,
        "client_status": "ESTABLISHED",
        "interaction_frequency": "REGULAR",
        "banking_seniority_years": 5
    },
    "personal_situation": {
        "marital_status": "MARRIED",
        "dependents_count": 2,
        "spouse_exists": True,
        "spouse_info": {
            "professional_status": "EMPLOYED",
            "monthly_income": 2500
        }
    },
    "professional_situation": {
        "professional_status": "EMPLOYEE_CDI",
        "sector": "TECHNOLOGY",
        "seniority_years": 8,
        "stability": "HIGH"
    },
    "financial_situation": {
        "monthly_income_net": 3500,
        "monthly_fixed_expenses": 1800,
        "existing_credits_total": 10000,
        "existing_credits_monthly_payment": 300,
        "debt_ratio": 0.086,
        "available_savings": 15000,
        "banking_history": "NO_INCIDENT"
    },
    "credit_request": {
        "credit_type": "PERSONAL",
        "amount_requested": 20000,
        "duration_months": 48,
        "purpose": "NECESSARY_EXPENSE"
    },
    "behavioral_indicators": {
        "stress_level": 2,
        "urgency_level": 3,
        "project_clarity": 4,
        "engagement_level": 5,
        "discourse_coherence": "HIGH"
    },
    "real_intention": {
        "main_motivation": "NECESSITY",
        "projection_capacity": "LONG_TERM"
    },
    "risk_checklist": {
        "professional_instability": False,
        "high_debt": False,
        "spouse_income_dependency": False,
        "non_priority_project": False,
        "excessive_urgency": False,
        "incoherent_discourse": False
    },
    "synthesis": {
        "global_risk_profile": "LOW",
        "theoretical_repayment_capacity": "GOOD"
    }
}


def main():
    print("="*60)
    print("ML MODEL INTEGRATION TEST")
    print("="*60)
    
    # Initialize ML agent
    print("\n1️⃣ Initializing ML Risk Agent...")
    agent = MLRiskAgent()
    
    if agent.model is None:
        print("   ❌ Model not loaded - check model file path")
        return
    
    print("   ✅ ML Model loaded successfully")
    
    # Extract features
    print("\n2️⃣ Extracting features from test application...")
    features_df = agent.extract_features(test_application)
    print(f"   ✅ Extracted {len(features_df.columns)} features")
    print(f"   Sample features: {list(features_df.columns[:5])}")
    
    # Make prediction
    print("\n3️⃣ Making prediction...")
    result = agent.predict(test_application)
    
    print("\n" + "="*60)
    print("PREDICTION RESULTS")
    print("="*60)
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n🎉 The ML model is ready for production use!")


if __name__ == "__main__":
    main()
