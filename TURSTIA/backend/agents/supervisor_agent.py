from datetime import datetime

from backend.agents.embedding_agent import EmbeddingAgent
from backend.agents.retrieval_agent import QdrantRetrievalAgent
from backend.agents.fraud_agent import FraudAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.scenario_agent import ScenarioAgent
from backend.agents.explanation_agent import ExplanationAgent
from backend.agents.audit_agent import AuditAgent

from backend.agents.document_agent import run_document_agent
from backend.agents.profile_fusion_agent import build_final_profile
from backend.utils.radar_builder import build_radar_points


class SupervisorAgent:
    """
    Orchestrateur central du pipeline crédit TRUSTIA
    """

    def __init__(self):
        self.embedding_agent = EmbeddingAgent()
        self.retrieval_agent = QdrantRetrievalAgent()
        self.fraud_agent = FraudAgent()
        self.risk_agent = RiskAgent()
        self.scenario_agent = ScenarioAgent()
        self.explanation_agent = ExplanationAgent()
        self.audit_agent = AuditAgent()

    # ======================================================
    # MAIN ENTRY
    # ======================================================
    def run(self, application_package: dict):

        case_id = application_package["case_id"]

        # ======================================================
        # 1️⃣ Document Intelligence
        # ======================================================
        doc_result = run_document_agent(
            case_id=case_id,
            documents=application_package.get("documents", [])
        )

        # ======================================================
        # 2️⃣ Profile Fusion
        # ======================================================
        fusion_result = build_final_profile(
            case_id=case_id,
            applicant_form=application_package.get("applicant_form", {}),
            loan_request=application_package.get("loan_request", {}),
            doc_signals=doc_result.doc_signals
        )

        final_profile = fusion_result.final_profile

        # ======================================================
        # 3️⃣ Embedding
        # ======================================================
        embedding_result = self.embedding_agent.run(
            chunks=[c.dict() for c in doc_result.chunks],
            final_profile=final_profile.dict(),
            loan_request=application_package.get("loan_request", {})
        )

        # ======================================================
        # 4️⃣ Retrieval (Qdrant)
        # ======================================================
        retrieval_result = self.retrieval_agent.run(
            case_id=case_id,
            case_vector=embedding_result["case_vector"],
            feature_payload=embedding_result["feature_payload"]
        )

        radar_points = build_radar_points(case_id, retrieval_result)

        # ======================================================
        # 5️⃣ FRAUD HARD STOP
        # ======================================================
        fraud_eval = self.fraud_agent.evaluate({
            "fraud_scores": [c["score"] for c in retrieval_result["similar_fraud_cases"]]
        })

        if fraud_eval["fraud_risk"] == "HIGH":

            confidence = min(0.95, 0.6 + 0.4 * retrieval_result["top_similarity"])

            decision = {
                "mode": "FRAUD",
                "decision": "REJECT",
                "confidence": round(confidence, 2),
                "fraud_summary": {
                    "top_similarity": retrieval_result["top_similarity"],
                    "similar_fraud_cases": retrieval_result["similar_fraud_cases"][:5]
                },
                "radar_points": radar_points
            }

            self._store_case(case_id, embedding_result, decision, final_profile, application_package, None)

            return self._finalize(case_id, decision)

        # ======================================================
        # 6️⃣ Risk Evaluation
        # ======================================================
        risk_result = self.risk_agent.evaluate(
            client_profile=final_profile.dict(),
            llm_summary={"top_similarity": retrieval_result["top_similarity"]}
        )

        default_prob = risk_result["default_probability"]

        # ======================================================
        # 7️⃣ COLD START
        # ======================================================
        if len(retrieval_result["similar_normal_cases"]) < 3 or default_prob > 0.6:

            confidence = max(0.3, retrieval_result["top_similarity"])

            decision = {
                "mode": "COLD_START",
                "decision": "HUMAN_REVIEW",
                "confidence": round(confidence, 2),
                "cold_start_summary": {
                    "reason": "Insufficient reliable historical similarity",
                    "similar_cases_count": len(retrieval_result["similar_normal_cases"]),
                    "top_similarity": retrieval_result["top_similarity"],
                    "risk_level_estimate": risk_result["risk_level"]
                },
                "radar_points": radar_points
            }

            self._store_case(case_id, embedding_result, decision, final_profile, application_package, default_prob)

            return self._finalize(case_id, decision)

        # ======================================================
        # 8️⃣ Scenario Simulation (NORMAL)
        # ======================================================
        stats_by_decision = self._build_stats_by_decision(
            retrieval_result["similar_normal_cases"] + retrieval_result["similar_fraud_cases"]
        )

        scenario_result = self.scenario_agent.simulate(
            stats_by_decision=stats_by_decision,
            default_probability=default_prob
        )

        decision = {
            "mode": "NORMAL",
            "decision": scenario_result["best_scenario"],
            "confidence": round(1 - default_prob, 2),
            "risk_summary": risk_result,
            "scenario_table": scenario_result["scenario_table"],
            "radar_points": radar_points
        }

        self._store_case(case_id, embedding_result, decision, final_profile, application_package, default_prob)

        return self._finalize(case_id, decision)

    # ======================================================
    # HELPERS
    # ======================================================
    def _build_stats_by_decision(self, cases):
        stats = {}

        for c in cases:
            decision = c.get("decision")
            if not decision:
                continue

            stats.setdefault(decision, {
                "count": 0,
                "defaults": 0,
                "total_loss": 0
            })

            stats[decision]["count"] += 1

            if c.get("outcome") == "DEFAULT":
                stats[decision]["defaults"] += 1
                stats[decision]["total_loss"] += c.get("loss_amount", 0)

        final_stats = {}
        for d, s in stats.items():
            n = s["count"]
            defaults = s["defaults"]
            final_stats[d] = {
                "n": n,
                "observed_default_rate": round(defaults / n, 2) if n else 0,
                "avg_loss_if_default": round(s["total_loss"] / defaults, 2) if defaults else 0
            }

        return final_stats

    def _store_case(self, case_id, embedding_result, decision, final_profile, application_package, default_probability):
        payload = {
            "case_id": case_id,
            "decision": decision["decision"],
            "fraud_label": decision["mode"] == "FRAUD",
            "outcome": None,
            "employment_type": final_profile.employment_type,
            "sector": final_profile.sector,
            "loan_amount": application_package["loan_request"].get("loan_amount"),
            "term_months": application_package["loan_request"].get("term_months"),
            "default_probability": default_probability,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.retrieval_agent.store_case(
            case_id=case_id,
            vector=embedding_result["case_vector"],
            payload=payload
        )

    def _finalize(self, case_id, decision):
        explanation = self.explanation_agent.explain(decision)
        audit = self.audit_agent.log(case_id, decision)

        return {
            "case_id": case_id,
            **decision,
            "explanation": explanation,
            "audit": audit
        }
