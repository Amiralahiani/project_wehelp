# backend/agents/ml_risk_agent.py
"""
ML Risk Agent - Integrates external ML model for credit risk prediction.
This agent extracts relevant features from ExpandedApplicationPackage and 
runs them through a trained ML model.
"""

import os
import pickle
import numpy as np
import pandas as pd
from typing import Dict, Any
from pathlib import Path


class MLRiskAgent:
    """
    Loads and runs ML model for credit risk assessment.
    Expected model: scikit-learn pipeline or similar that accepts DataFrame input.
    """

    def __init__(self, model_path: str = None):
        """
        Initialize the ML Risk Agent.
        
        Args:
            model_path: Path to the saved ML model (.pkl, .joblib, etc.)
        """
        self.model_path = model_path or self._get_default_model_path()
        self.model = None
        self._load_model()

    def _get_default_model_path(self) -> str:
        """Get default model path in backend/models/"""
        backend_dir = Path(__file__).parent.parent
        return str(backend_dir / "models" / "credit_risk_model.pkl")

    def _load_model(self):
        """Load the ML model from disk."""
        if not os.path.exists(self.model_path):
            print(f"⚠️ ML Model not found at {self.model_path}")
            print("⚠️ Running in PLACEHOLDER mode - will return dummy predictions")
            self.model = None
            return

        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"✅ ML Model loaded successfully from {self.model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None

    def extract_features(self, application: Dict[str, Any]) -> pd.DataFrame:
        """
        Extract and engineer features from ExpandedApplicationPackage for ML model.
        
        Args:
            application: Dictionary representation of ExpandedApplicationPackage
            
        Returns:
            DataFrame with features for ML model
        """
        # Extract nested data
        client = application.get("client_identity", {})
        personal = application.get("personal_situation", {})
        professional = application.get("professional_situation", {})
        financial = application.get("financial_situation", {})
        credit = application.get("credit_request", {})
        behavioral = application.get("behavioral_indicators", {})
        intention = application.get("real_intention", {})
        risks = application.get("risk_checklist", {})
        synthesis = application.get("synthesis", {})

        # Build feature dictionary
        features = {
            # Client identity
            'age': client.get('age', 0),
            'banking_seniority_years': client.get('banking_seniority_years', 0) or 0,
            'client_status_is_new': 1 if client.get('client_status') == 'NEW' else 0,
            'interaction_frequency_rare': 1 if client.get('interaction_frequency') == 'RARE' else 0,

            # Personal situation
            'dependents_count': personal.get('dependents_count', 0),
            'has_spouse': 1 if personal.get('spouse_exists') else 0,
            'spouse_income': personal.get('spouse_info', {}).get('monthly_income', 0) if personal.get('spouse_exists') else 0,
            'is_married': 1 if personal.get('marital_status') == 'MARRIED' else 0,

            # Professional situation
            'is_employed_cdi': 1 if professional.get('professional_status') == 'EMPLOYEE_CDI' else 0,
            'is_unemployed': 1 if professional.get('professional_status') == 'UNEMPLOYED' else 0,
            'job_seniority_years': professional.get('seniority_years', 0) or 0,
            'job_stability_high': 1 if professional.get('stability') == 'HIGH' else 0,
            'job_stability_low': 1 if professional.get('stability') == 'LOW' else 0,

            # Financial situation
            'monthly_income': financial.get('monthly_income_net', 0),
            'monthly_expenses': financial.get('monthly_fixed_expenses', 0),
            'existing_debt': financial.get('existing_credits_total', 0) or 0,
            'debt_monthly_payment': financial.get('existing_credits_monthly_payment', 0) or 0,
            'debt_ratio': financial.get('debt_ratio', 0) or 0,
            'available_savings': financial.get('available_savings', 0) or 0,
            'has_banking_incidents': 0 if financial.get('banking_history') == 'NO_INCIDENT' else 1,
            'major_banking_incidents': 1 if financial.get('banking_history') == 'MAJOR_INCIDENTS' else 0,

            # Credit request
            'amount_requested': credit.get('amount_requested', 0),
            'duration_months': credit.get('duration_months', 0),
            'is_real_estate': 1 if credit.get('credit_type') == 'REAL_ESTATE' else 0,
            'is_investment': 1 if credit.get('purpose') == 'INVESTMENT' else 0,
            'is_comfort_expense': 1 if credit.get('purpose') == 'COMFORT_EXPENSE' else 0,

            # Behavioral indicators
            'stress_level': int(behavioral.get('stress_level', 3)),
            'urgency_level': int(behavioral.get('urgency_level', 3)),
            'project_clarity': int(behavioral.get('project_clarity', 3)),
            'engagement_level': int(behavioral.get('engagement_level', 3)),
            'low_coherence': 1 if behavioral.get('discourse_coherence') == 'LOW' else 0,

            # Real intention
            'external_pressure': 1 if intention.get('main_motivation') == 'EXTERNAL_PRESSURE' else 0,
            'short_term_only': 1 if intention.get('projection_capacity') == 'SHORT_TERM_ONLY' else 0,

            # Risk checklist (binary flags)
            'risk_professional_instability': 1 if risks.get('professional_instability') else 0,
            'risk_high_debt': 1 if risks.get('high_debt') else 0,
            'risk_spouse_dependency': 1 if risks.get('spouse_income_dependency') else 0,
            'risk_non_priority': 1 if risks.get('non_priority_project') else 0,
            'risk_excessive_urgency': 1 if risks.get('excessive_urgency') else 0,
            'risk_incoherent': 1 if risks.get('incoherent_discourse') else 0,

            # Synthesis
            'global_risk_high': 1 if synthesis.get('global_risk_profile') == 'HIGH' else 0,
            'repayment_capacity_insufficient': 1 if synthesis.get('theoretical_repayment_capacity') == 'INSUFFICIENT' else 0,
        }

        # Derived features
        if features['monthly_income'] > 0:
            features['expense_ratio'] = features['monthly_expenses'] / features['monthly_income']
            features['credit_to_income_ratio'] = features['amount_requested'] / (features['monthly_income'] * 12)
        else:
            features['expense_ratio'] = 1.0
            features['credit_to_income_ratio'] = 10.0

        # Risk count
        features['total_risk_flags'] = sum([
            features['risk_professional_instability'],
            features['risk_high_debt'],
            features['risk_spouse_dependency'],
            features['risk_non_priority'],
            features['risk_excessive_urgency'],
            features['risk_incoherent']
        ])

        return pd.DataFrame([features])

    def predict(self, application: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run ML model prediction on application data.
        
        Args:
            application: Dictionary representation of ExpandedApplicationPackage
            
        Returns:
            Dictionary with ML prediction results
        """
        # Extract features
        features_df = self.extract_features(application)

        # Run model or return placeholder
        if self.model is None:
            # PLACEHOLDER MODE - Return dummy prediction
            return self._placeholder_prediction(features_df)

        try:
            # Real model prediction
            # Assumes model has .predict_proba() method (classification)
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(features_df)[0]
                default_probability = float(proba[1])  # Probability of default
                prediction = 1 if default_probability > 0.5 else 0
            else:
                prediction = int(self.model.predict(features_df)[0])
                default_probability = float(prediction)

            # Determine risk level
            if default_probability < 0.3:
                risk_level = "LOW"
            elif default_probability < 0.6:
                risk_level = "MEDIUM"
            else:
                risk_level = "HIGH"

            return {
                "ml_risk_score": round(default_probability, 3),
                "ml_risk_level": risk_level,
                "ml_prediction": "REJECT" if prediction == 1 else "ACCEPT",
                "model_used": "ML_MODEL",
                "feature_count": len(features_df.columns)
            }

        except Exception as e:
            print(f"❌ Error during ML prediction: {e}")
            return self._placeholder_prediction(features_df)

    def _placeholder_prediction(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate placeholder prediction when model is not available.
        Uses simple heuristics based on features.
        """
        # Simple risk calculation based on key features
        risk_score = 0.3  # Base risk

        # Adjust based on key factors
        if features_df['total_risk_flags'].iloc[0] >= 3:
            risk_score += 0.3
        if features_df['debt_ratio'].iloc[0] > 0.5:
            risk_score += 0.2
        if features_df['is_unemployed'].iloc[0] == 1:
            risk_score += 0.3
        if features_df['major_banking_incidents'].iloc[0] == 1:
            risk_score += 0.25
        if features_df['job_stability_low'].iloc[0] == 1:
            risk_score += 0.15

        # Cap at 1.0
        risk_score = min(risk_score, 1.0)

        if risk_score < 0.3:
            risk_level = "LOW"
        elif risk_score < 0.6:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        return {
            "ml_risk_score": round(risk_score, 3),
            "ml_risk_level": risk_level,
            "ml_prediction": "REJECT" if risk_score > 0.6 else "ACCEPT",
            "model_used": "PLACEHOLDER_HEURISTIC",
            "feature_count": len(features_df.columns),
            "warning": "Using placeholder prediction - ML model not loaded"
        }
