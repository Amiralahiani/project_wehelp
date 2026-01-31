# backend/tests/test_persona4_agents.py

from agents.fraud_agent import FraudAgent
from agents.decision_agent_fraud_cold import DecisionAgentFraudCold
from agents.explanation_agent import ExplanationAgent
from agents.audit_agent import AuditAgent

def test_fraud_case():
    print("\n=== TEST CAS FRAUDE ===")

    fraud_agent = FraudAgent()
    decision_agent = DecisionAgentFraudCold()
    explanation_agent = ExplanationAgent()
    audit_agent = AuditAgent()

    payload = {
        "case_id": "CASE_FRAUD_001",
        "top_similarity": 0.88,
        "retrieval_result": {
            "fraud_scores": [0.91, 0.87]
        }
    }

    fraud_result = fraud_agent.evaluate(payload["retrieval_result"])
    decision = decision_agent.decide(
        payload["top_similarity"],
        fraud_result["fraud_risk"]
    )

    explanation = explanation_agent.explain(decision)
    audit = audit_agent.log(payload["case_id"], decision)

    print("Fraud Result :", fraud_result)
    print("Decision     :", decision)
    print("Explanation  :", explanation)
    print("Audit Log    :", audit)


def test_cold_start_case():
    print("\n=== TEST CAS COLD START ===")

    fraud_agent = FraudAgent()
    decision_agent = DecisionAgentFraudCold()
    explanation_agent = ExplanationAgent()
    audit_agent = AuditAgent()

    payload = {
        "case_id": "CASE_COLD_001",
        "top_similarity": 0.60,
        "retrieval_result": {
            "fraud_scores": []
        }
    }

    fraud_result = fraud_agent.evaluate(payload["retrieval_result"])
    decision = decision_agent.decide(
        payload["top_similarity"],
        fraud_result["fraud_risk"]
    )

    explanation = explanation_agent.explain(decision)
    audit = audit_agent.log(payload["case_id"], decision)

    print("Fraud Result :", fraud_result)
    print("Decision     :", decision)
    print("Explanation  :", explanation)
    print("Audit Log    :", audit)


def test_normal_case():
    print("\n=== TEST CAS NORMAL ===")

    fraud_agent = FraudAgent()
    decision_agent = DecisionAgentFraudCold()

    payload = {
        "case_id": "CASE_NORMAL_001",
        "top_similarity": 0.85,
        "retrieval_result": {
            "fraud_scores": [0.20]
        }
    }

    fraud_result = fraud_agent.evaluate(payload["retrieval_result"])
    decision = decision_agent.decide(
        payload["top_similarity"],
        fraud_result["fraud_risk"]
    )

    print("Fraud Result :", fraud_result)
    print("Decision     :", decision)
    print("➡️ NORMAL PATH (handled by Personna 3)")


if __name__ == "__main__":
    test_fraud_case()
    test_cold_start_case()
    test_normal_case()
