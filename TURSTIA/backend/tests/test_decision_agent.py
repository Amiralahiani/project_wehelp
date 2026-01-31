from backend.agents.decision_agent import DecisionAgent

def test_decision_agent():
    agent = DecisionAgent()

    # =========================
    # CAS 1 — NORMAL
    # =========================
    result_normal = agent.run(
        top_similarity=0.85,
        fraud_result={
            "fraud_risk_level": "LOW",
            "fraud_similarity": 0.2,
            "anomaly_score": 0.3
        },
        scenario_result={
            "best_scenario": "ACCEPT_WITH_GUARANTEE"
        },
        risk_result={
            "risk_level": "MEDIUM",
            "default_probability": 0.25
        }
    )
    print("NORMAL:", result_normal)

    # =========================
    # CAS 2 — COLD START
    # =========================
    result_cold = agent.run(
        top_similarity=0.30,   
        fraud_result={
            "fraud_risk_level": "LOW",
            "fraud_similarity": 0.1,
            "anomaly_score": 0.2
        },
        scenario_result={
            "best_scenario": "ACCEPT_WITH_GUARANTEE"
        },
        risk_result={
            "risk_level": "LOW",
            "default_probability": 0.10
        }
    )
    print("COLD START:", result_cold)

    # =========================
    # CAS 3 — FRAUD STOP
    # =========================
    result_fraud = agent.run(
        top_similarity=0.90,
        fraud_result={
            "fraud_risk_level": "HIGH",  # déclenche FRAUD_STOP
            "fraud_similarity": 0.92,
            "anomaly_score": 0.85
        },
        scenario_result={
            "best_scenario": "REJECT"
        },
        risk_result={
            "risk_level": "HIGH",
            "default_probability": 0.80
        }
    )
    print("FRAUD STOP:", result_fraud)


if __name__ == "__main__":
    test_decision_agent()
    print("DecisionAgent tests completed")
