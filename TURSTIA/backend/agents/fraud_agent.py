from backend.config import FRAUD_SIMILARITY_THRESHOLD

class FraudAgent:
    def evaluate(self, retrieval_result: dict):
        """
        retrieval_result contient les résultats Qdrant
        """
        fraud_scores = retrieval_result.get("fraud_scores", [])

        if not fraud_scores:
            return {
                "fraud_risk": "LOW",
                "reason": "No fraud cases retrieved"
            }

        max_score = max(fraud_scores)

        if max_score >= FRAUD_SIMILARITY_THRESHOLD:
            return {
                "fraud_risk": "HIGH",
                "reason": f"High similarity with fraud cases ({max_score})"
            }

        return {
            "fraud_risk": "LOW",
            "reason": "Fraud similarity below threshold"
        }
