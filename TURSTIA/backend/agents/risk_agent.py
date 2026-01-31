# backend/agents/risk_agent.py

class RiskAgent:

    def evaluate(self, client_profile, llm_summary):

        # ✅ Accès robuste avec fallback
        income = client_profile.get("monthly_income") \
                 or client_profile.get("income") \
                 or client_profile.get("monthly_income_declared") \
                 or 0

        expenses = client_profile.get("monthly_expenses") \
                   or client_profile.get("expenses") \
                   or client_profile.get("monthly_expenses_declared") \
                   or 0

        debt_ratio = client_profile.get("debt_ratio", 0.0)
        job_stability = client_profile.get("stability_score", 0.5)

        risk = 0.1

        if debt_ratio > 0.5:
            risk += 0.15

        if income > 0 and expenses > income * 0.6:
            risk += 0.1

        if job_stability < 0.5:
            risk += 0.15

        similarity = llm_summary.get("top_similarity", 0)

        if similarity > 0.7:
            risk -= 0.05
        else:
            risk += 0.05

        # Clamp
        risk = min(max(risk, 0), 1)

        if risk < 0.2:
            level = "LOW"
        elif risk < 0.4:
            level = "MEDIUM"
        else:
            level = "HIGH"

        risk_factors = []
        if debt_ratio > 0.5:
            risk_factors.append("high_debt_ratio")
        if income > 0 and expenses > income * 0.6:
            risk_factors.append("high_expenses")
        if job_stability < 0.5:
            risk_factors.append("low_job_stability")

        return {
            "risk_score": round(risk, 2),
            "risk_level": level,
            "default_probability": round(risk, 2),
            "risk_factors": risk_factors,
            "llm_insights_used": True
        }
