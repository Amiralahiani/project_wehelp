from backend.agents.risk_agent import RiskAgent
from backend.agents.scenario_agent import ScenarioAgent
from backend.agents.decision_agent import DecisionAgent



# Exemple fictif
client_profile = {
    "monthly_income": 3000,
    "monthly_expenses": 1500,
    "debt_ratio": 0.4,
    "job_stability": 0.7
}
llm_summary = {"top_similarity": 0.8}
stats_by_decision = {
    "ACCEPT": {"n": 10, "observed_default_rate": 0.1, "avg_loss_if_default": 1000},
    "REJECT": {"n": 5, "observed_default_rate": 0.3, "avg_loss_if_default": 5000},
    "ACCEPT_WITH_GUARANTEE": {"n": 8, "observed_default_rate": 0.15, "avg_loss_if_default": 2000}
}
fraud_result = {"fraud_risk_level": "LOW", "fraud_similarity": 0.2, "anomaly_score": 0.1}

# 1. Risk
risk_agent = RiskAgent()
risk_result = risk_agent.evaluate(client_profile, llm_summary)
print("RISK RESULT:", risk_result)

# 2. Scenario
scenario_agent = ScenarioAgent()
scenario_result = scenario_agent.simulate(stats_by_decision, risk_result["default_probability"])
print("SCENARIO RESULT:", scenario_result)

# 3. Decision
decision_agent = DecisionAgent()
decision_result = decision_agent.run(
    top_similarity=llm_summary["top_similarity"],
    fraud_result=fraud_result,
    scenario_result=scenario_result,
    risk_result=risk_result
)
print("DECISION RESULT:", decision_result)
