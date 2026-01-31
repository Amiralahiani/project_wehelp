# ======================================
# Decision & Policy Agent
# ======================================



from backend.config import (
    SIMILARITY_THRESHOLD,
    FRAUD_SIMILARITY_THRESHOLD,
)


class DecisionAgent:
    """
    Branchements finaux : NORMAL / FRAUD_STOP / COLD_START
    """

    def run(self, top_similarity, fraud_result, scenario_result, risk_result):
        """
        Inputs:
        - top_similarity: float
        - fraud_result: { fraud_risk_level, fraud_similarity, anomaly_score }
        - scenario_result: { best_scenario }
        - risk_result: { risk_level, default_probability }

        Output: DecisionResponse | FraudResponse | ColdStartResponse
        """

        fraud_risk_level = fraud_result["fraud_risk_level"]
        anomaly_score = fraud_result["anomaly_score"]
        best_scenario = scenario_result["best_scenario"]
        risk_level = risk_result["risk_level"]

        # ===============================
        # FRAUD STOP
        # ===============================
        if fraud_risk_level == "HIGH" or anomaly_score >= FRAUD_SIMILARITY_THRESHOLD:
            return {
                "mode": "FRAUD_STOP",
                "status": "SUSPENDED",
                "fraud_risk_level": fraud_risk_level,
                "confidence": round(max(top_similarity, fraud_result["fraud_similarity"]), 2),
                "action": "SEND_TO_INVESTIGATION"
            }

        # ===============================
        # COLD START
        # ===============================
        if top_similarity < SIMILARITY_THRESHOLD:
            return {
                "mode": "COLD_START",
                "ai_recommendation": best_scenario,
                "confidence": round(top_similarity, 2),
                "human_validation_required": True,
                "reason": "No similar cases above threshold"
            }

        # ===============================
        # NORMAL
        # ===============================
        confidence = self._compute_confidence(top_similarity, risk_level)

        conditions = self._build_conditions(best_scenario)

        return {
            "mode": "NORMAL",
            "final_decision": best_scenario,
            "confidence": confidence,
            "conditions": conditions
        }

    # -----------------------
    # Helpers
    # -----------------------

    def _compute_confidence(self, top_similarity, risk_level):
        if risk_level == "LOW":
            conf = top_similarity
        elif risk_level == "MEDIUM":
            conf = top_similarity - 0.05
        else:  # HIGH
            conf = top_similarity - 0.15
        return round(max(conf, 0), 2)

    def _build_conditions(self, best_scenario):
        if best_scenario == "ACCEPT":
            return ["no_collateral", "max_amount=10000", "term<=36m"]
        elif best_scenario == "ACCEPT_WITH_GUARANTEE":
            return ["collateral_required", "max_amount=8000", "term<=24m"]
        else:
            return ["application_rejected"]




# from backend.config import (
#     SIMILARITY_THRESHOLD,
#     FRAUD_SIMILARITY_THRESHOLD
# )


# class DecisionAgent:

#     def run(self, retrieval_result: dict):

#         top_similarity = retrieval_result.get("top_similarity", 0.0)
#         similar_fraud_cases = retrieval_result.get("similar_fraud_cases", [])

#         # ===============================
#         # FRAUD STOP
#         # ===============================
#         if similar_fraud_cases:
#             max_fraud_score = max(c["score"] for c in similar_fraud_cases)

#             if max_fraud_score >= FRAUD_SIMILARITY_THRESHOLD:
#                 return {
#                     "mode": "FRAUD_STOP",
#                     "confidence": round(max_fraud_score, 3),
#                     "reason": "High similarity with known fraud cases"
#                 }

#         # ===============================
#         # COLD START
#         # ===============================
#         if top_similarity < SIMILARITY_THRESHOLD:
#             return {
#                 "mode": "COLD_START",
#                 "confidence": round(top_similarity, 3),
#                 "reason": "No sufficiently similar historical cases",
#                 "human_validation_required": True
#             }

#         # ===============================
#         #  NORMAL
#         # ===============================
#         return {
#             "mode": "NORMAL",
#             "confidence": round(top_similarity, 3),
#             "reason": "Sufficient similarity with historical cases"
#         }
    
#     def decide(self, top_similarity, fraud_risk_level, best_scenario, risk_result):
#         """
#         Détermine la décision finale pour un dossier NORMAL
#         """

#         # --- Vérification mode NORMAL ---
#         if fraud_risk_level != "LOW" or top_similarity < 0.75:
#             return {"mode": "NON_NORMAL"}

#         mode = "NORMAL"
#         risk_level = risk_result["risk_level"]

#         # --- Calcul confidence clair ---
#         if risk_level == "LOW":
#             confidence = top_similarity
#         elif risk_level == "MEDIUM":
#             confidence = top_similarity - 0.05
#         else:  # HIGH
#             confidence = top_similarity - 0.15

#         confidence = round(max(confidence, 0), 2)

#         # --- Conditions selon scénario ---
#         if best_scenario == "ACCEPT":
#             conditions = [
#                 "no_collateral",
#                 "max_amount=10000",
#                 "term<=36m"
#             ]
#         elif best_scenario == "ACCEPT_WITH_GUARANTEE":
#             conditions = [
#                 "collateral_required",
#                 "max_amount=8000",
#                 "term<=24m"
#             ]
#         else:  # REJECT
#             conditions = ["application_rejected"]

#         return {
#             "mode": mode,
#             "final_decision": best_scenario,
#             "confidence": confidence,
#             "conditions": conditions
#         }