# tests/test_scenario_agent_full.py

from backend.agents.risk_agent import RiskAgent
from backend.agents.scenario_agent import ScenarioAgent
from backend.agents.decision_agent import DecisionAgent

risk_agent = RiskAgent()
scenario_agent = ScenarioAgent()
decision_agent = DecisionAgent()

stats_by_decision = {
    "ACCEPT": {"n": 100, "observed_default_rate": 0.10, "avg_loss_if_default": 5000},
    "REJECT": {"n": 50, "avg_loss_if_default": 0},
    "ACCEPT_WITH_GUARANTEE": {"n": 80, "observed_default_rate": 0.20, "avg_loss_if_default": 3000}
}

cases = [
    {
        "name": "LOW RISK",
        "profile": {"monthly_income": 5000, "monthly_expenses": 1500, "debt_ratio": 0.2, "job_stability": 0.9},
        "similarity": 0.85,
        "fraud": "LOW"
    },
    {
        "name": "MEDIUM RISK",
        "profile": {"monthly_income": 3000, "monthly_expenses": 2000, "debt_ratio": 0.6, "job_stability": 0.6},
        "similarity": 0.78,
        "fraud": "LOW"
    },
    {
        "name": "HIGH RISK - ACCEPT_WITH_REJECT",
        "profile": {"monthly_income": 2000, "monthly_expenses": 1800, "debt_ratio": 0.8, "job_stability": 0.3},
        "similarity": 0.80,  # >= 0.75 pour que le mode soit NORMAL
        "fraud": "LOW"
    },
    {
        "name": "FRAUD CASE",
        "profile": {"monthly_income": 6000, "monthly_expenses": 1000, "debt_ratio": 0.2, "job_stability": 0.95},
        "similarity": 0.95,
        "fraud": "HIGH"
    }
]

for case in cases:
    print(f"\n=== {case['name']} ===")
    
    # 1️⃣ Calcul du risque
    risk_result = risk_agent.evaluate(case["profile"], {"top_similarity": case["similarity"]})
    
    # 2️⃣ Simulation des scénarios (si pas fraude)
    if case["fraud"] == "LOW":
        scenario_result = scenario_agent.simulate(stats_by_decision, risk_result["default_probability"])
        best_scenario = scenario_result["best_scenario"]
    else:
        scenario_result = None
        best_scenario = None
    
    # 3️⃣ Décision finale
    decision_result = decision_agent.decide(
        top_similarity=case["similarity"],
        fraud_risk_level=case["fraud"],
        best_scenario=best_scenario,
        risk_result=risk_result
    )
    
    # --- Affichage ---
    print("Risk:", risk_result)
    print("Scenario Table:", scenario_result["scenario_table"] if scenario_result else "FRAUD - No scenario")
    print("Decision:", decision_result)
