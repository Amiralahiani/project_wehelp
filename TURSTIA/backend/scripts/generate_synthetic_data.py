"""
Synthetic Credit Dataset Generator
Generates realistic synthetic credit application data for ML training
"""

import pandas as pd
import numpy as np
from pathlib import Path
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


def generate_synthetic_dataset(n_samples: int = 2000) -> pd.DataFrame:
    """
    Generate synthetic credit application dataset with realistic correlations.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        DataFrame with synthetic credit applications
    """
    
    data = []
    
    for _ in range(n_samples):
        # Client identity
        age = np.random.normal(40, 12)
        age = max(18, min(70, age))  # Clip to realistic range
        
        banking_seniority = np.random.exponential(5)
        banking_seniority = min(banking_seniority, age - 18)  # Can't be older than adult age
        
        client_status_is_new = 1 if banking_seniority < 1 else 0
        interaction_frequency_rare = np.random.choice([0, 1], p=[0.6, 0.4])
        
        # Personal situation
        dependents_count = np.random.choice([0, 1, 2, 3, 4], p=[0.25, 0.25, 0.3, 0.15, 0.05])
        is_married = np.random.choice([0, 1], p=[0.45, 0.55])
        has_spouse = is_married
        spouse_income = 0
        if has_spouse:
            spouse_income = max(0, np.random.normal(2500, 800))
        
        # Professional situation
        employment_probs = [0.65, 0.05, 0.15, 0.10, 0.05]  # CDI, CDD, Independent, Retired, Unemployed
        employment = np.random.choice([0, 1, 2, 3, 4], p=employment_probs)
        
        is_employed_cdi = 1 if employment == 0 else 0
        is_unemployed = 1 if employment == 4 else 0
        
        if is_unemployed:
            job_seniority_years = 0
            job_stability_high = 0
            job_stability_low = 1
        else:
            job_seniority_years = max(0, np.random.exponential(5))
            if job_seniority_years > 5:
                job_stability_high = 1
                job_stability_low = 0
            elif job_seniority_years < 2:
                job_stability_high = 0
                job_stability_low = 1
            else:
                job_stability_high = 0
                job_stability_low = 0
        
        # Financial situation (correlated with employment)
        if is_unemployed:
            monthly_income = max(0, np.random.normal(800, 200))  # Unemployment benefits
        elif is_employed_cdi:
            monthly_income = max(1000, np.random.normal(3000, 1000))
        else:
            monthly_income = max(800, np.random.normal(2000, 800))
        
        # Expenses proportional to income and dependents
        base_expenses = monthly_income * np.random.uniform(0.4, 0.7)
        dependent_expenses = dependents_count * 300
        monthly_expenses = base_expenses + dependent_expenses
        
        # Existing debt
        has_debt = np.random.choice([0, 1], p=[0.6, 0.4])
        if has_debt:
            existing_debt = np.random.uniform(2000, 50000)
            debt_monthly_payment = existing_debt / np.random.uniform(12, 60)
        else:
            existing_debt = 0
            debt_monthly_payment = 0
        
        debt_ratio = debt_monthly_payment / monthly_income if monthly_income > 0 else 0
        
        # Savings
        available_savings = max(0, np.random.exponential(5000))
        
        # Banking incidents
        incident_prob = 0.15 if debt_ratio > 0.5 else 0.05
        has_banking_incidents = np.random.choice([0, 1], p=[1-incident_prob, incident_prob])
        major_banking_incidents = 1 if (has_banking_incidents and np.random.random() < 0.3) else 0
        
        # Credit request
        amount_requested = max(1000, np.random.lognormal(8.5, 0.8))
        duration_months = np.random.choice([12, 24, 36, 48, 60, 72, 84], p=[0.15, 0.25, 0.25, 0.15, 0.10, 0.05, 0.05])
        
        is_real_estate = np.random.choice([0, 1], p=[0.7, 0.3])
        is_investment = np.random.choice([0, 1], p=[0.85, 0.15])
        is_comfort_expense = np.random.choice([0, 1], p=[0.7, 0.3])
        
        # Behavioral indicators (1-5 scale)
        stress_level = np.random.randint(1, 6)
        urgency_level = np.random.randint(1, 6)
        project_clarity = np.random.randint(1, 6)
        engagement_level = np.random.randint(1, 6)
        low_coherence = 1 if np.random.random() < 0.2 else 0
        
        # Real intention
        external_pressure = 1 if (urgency_level > 3 and stress_level > 3) else 0
        short_term_only = 1 if project_clarity < 3 else 0
        
        # Risk checklist
        risk_professional_instability = 1 if (is_unemployed or job_stability_low) else 0
        risk_high_debt = 1 if debt_ratio > 0.5 else 0
        risk_spouse_dependency = 1 if (has_spouse and spouse_income > monthly_income * 1.5) else 0
        risk_non_priority = 1 if is_comfort_expense else 0
        risk_excessive_urgency = 1 if urgency_level >= 5 else 0
        risk_incoherent = low_coherence
        
        total_risk_flags = sum([
            risk_professional_instability,
            risk_high_debt,
            risk_spouse_dependency,
            risk_non_priority,
            risk_excessive_urgency,
            risk_incoherent
        ])
        
        # Synthesis
        global_risk_high = 1 if total_risk_flags >= 3 else 0
        repayment_capacity_insufficient = 1 if debt_ratio > 0.6 else 0
        
        # Derived features
        expense_ratio = monthly_expenses / monthly_income if monthly_income > 0 else 1.0
        credit_to_income_ratio = amount_requested / (monthly_income * 12) if monthly_income > 0 else 10.0
        
        # TARGET VARIABLE: Default probability (realistic risk model)
        # Higher risk = higher chance of default
        base_default_prob = 0.1
        
        # Risk factors increase default probability
        if is_unemployed:
            base_default_prob += 0.3
        if debt_ratio > 0.5:
            base_default_prob += 0.25
        if major_banking_incidents:
            base_default_prob += 0.3
        if total_risk_flags >= 3:
            base_default_prob += 0.2
        if credit_to_income_ratio > 3:
            base_default_prob += 0.15
        if job_stability_low and not is_unemployed:
            base_default_prob += 0.1
        if age < 25 or age > 60:
            base_default_prob += 0.05
        if available_savings < 1000:
            base_default_prob += 0.1
        
        # Protective factors decrease default probability
        if is_employed_cdi:
            base_default_prob -= 0.1
        if job_stability_high:
            base_default_prob -= 0.05
        if available_savings > 10000:
            base_default_prob -= 0.1
        if debt_ratio < 0.2:
            base_default_prob -= 0.05
        
        # Clip to [0, 1]
        default_prob = max(0, min(1, base_default_prob))
        
        # Sample default outcome
        default = 1 if np.random.random() < default_prob else 0
        
        # Assemble row
        row = {
            'age': int(age),
            'banking_seniority_years': round(banking_seniority, 1),
            'client_status_is_new': client_status_is_new,
            'interaction_frequency_rare': interaction_frequency_rare,
            'dependents_count': dependents_count,
            'has_spouse': has_spouse,
            'spouse_income': round(spouse_income, 2),
            'is_married': is_married,
            'is_employed_cdi': is_employed_cdi,
            'is_unemployed': is_unemployed,
            'job_seniority_years': round(job_seniority_years, 1),
            'job_stability_high': job_stability_high,
            'job_stability_low': job_stability_low,
            'monthly_income': round(monthly_income, 2),
            'monthly_expenses': round(monthly_expenses, 2),
            'existing_debt': round(existing_debt, 2),
            'debt_monthly_payment': round(debt_monthly_payment, 2),
            'debt_ratio': round(debt_ratio, 3),
            'available_savings': round(available_savings, 2),
            'has_banking_incidents': has_banking_incidents,
            'major_banking_incidents': major_banking_incidents,
            'amount_requested': round(amount_requested, 2),
            'duration_months': duration_months,
            'is_real_estate': is_real_estate,
            'is_investment': is_investment,
            'is_comfort_expense': is_comfort_expense,
            'stress_level': stress_level,
            'urgency_level': urgency_level,
            'project_clarity': project_clarity,
            'engagement_level': engagement_level,
            'low_coherence': low_coherence,
            'external_pressure': external_pressure,
            'short_term_only': short_term_only,
            'risk_professional_instability': risk_professional_instability,
            'risk_high_debt': risk_high_debt,
            'risk_spouse_dependency': risk_spouse_dependency,
            'risk_non_priority': risk_non_priority,
            'risk_excessive_urgency': risk_excessive_urgency,
            'risk_incoherent': risk_incoherent,
            'total_risk_flags': total_risk_flags,
            'global_risk_high': global_risk_high,
            'repayment_capacity_insufficient': repayment_capacity_insufficient,
            'expense_ratio': round(expense_ratio, 3),
            'credit_to_income_ratio': round(credit_to_income_ratio, 3),
            'default': default  # TARGET
        }
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Print statistics
    print(f"\n📊 Generated {len(df)} synthetic credit applications")
    print(f"   Default rate: {df['default'].mean():.2%}")
    print(f"   Avg age: {df['age'].mean():.1f} years")
    print(f"   Avg monthly income: €{df['monthly_income'].mean():.0f}")
    print(f"   Avg credit amount: €{df['amount_requested'].mean():.0f}")
    print(f"   Unemployment rate: {df['is_unemployed'].mean():.1%}")
    
    return df


if __name__ == "__main__":
    # Generate dataset
    print("🔧 Generating synthetic credit dataset...")
    df = generate_synthetic_dataset(n_samples=2000)
    
    # Create data directory
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Save to CSV
    output_path = data_dir / "synthetic_credit_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Dataset saved to: {output_path}")
    print(f"   Shape: {df.shape}")
    print(f"   Features: {df.shape[1] - 1} (+ 1 target)")
