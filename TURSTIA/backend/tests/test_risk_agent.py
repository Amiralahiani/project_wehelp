from agents.risk_agent import RiskAgent

# 1️⃣ INPUTS DE TEST (FAUX CLIENT)
client_profile = {
    "monthly_income": 2000,
    "monthly_expenses": 1200,
    "debt_ratio": 0.6,
    "job_stability": 0.8
}

# 2️⃣ FAUX RÉSULTAT LLM (SIMILARITY)
llm_summary = {
    "top_similarity": 0.82
}

# 3️⃣ TEST
agent = RiskAgent()
result = agent.evaluate(client_profile, llm_summary)

print("Résultat du Risk Agent :", result)
