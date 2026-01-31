from backend.config import SIMILARITY_THRESHOLD

class DecisionAgentFraudCold:

    def decide(self, top_similarity: float, fraud_risk: str):
        if fraud_risk == "HIGH":
            return {
                "mode": "FRAUD",
                "decision": "REJECT",
                "confidence": 0.95
            }

        if top_similarity < SIMILARITY_THRESHOLD:
            return {
                "mode": "COLD_START",
                "decision": "HUMAN_REVIEW",
                "confidence": 0.50
            }

        return None  # laisse la main au NORMAL (Personne 3)
