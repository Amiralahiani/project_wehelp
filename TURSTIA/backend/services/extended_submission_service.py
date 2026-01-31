# backend/services/extended_submission_service.py
"""
Extended Submission Service - Orchestrates dual-pipeline credit evaluation:
1. ML Risk Model Pipeline (structured data)
2. Qdrant/RAG Pipeline (document + text summary)

Combines results from both pipelines for final decision.
"""

from typing import Dict, Any
from backend.agents.ml_risk_agent import MLRiskAgent
from backend.agents.embedding_agent import EmbeddingAgent
from backend.agents.retrieval_agent import RetrievalAgent
from backend.agents.fraud_agent import FraudAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.scenario_agent import ScenarioAgent
from backend.agents.decision_agent import DecisionAgent


class ExtendedSubmissionService:
    """
    Coordinates the evaluation of ExpandedApplicationPackage through
    both ML and traditional Qdrant-based pipelines.
    """

    def __init__(self):
        # Initialize agents for both pipelines
        self.ml_agent = MLRiskAgent()
        self.embedding_agent = EmbeddingAgent()
        self.retrieval_agent = RetrievalAgent()
        self.fraud_agent = FraudAgent()
        self.risk_agent = RiskAgent()
        self.scenario_agent = ScenarioAgent()
        self.decision_agent = DecisionAgent()

    def process_application(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process application through both pipelines and combine results.
        
        Args:
            application_data: Dictionary of ExpandedApplicationPackage
            
        Returns:
            Combined decision result
        """
        case_id = application_data.get("case_id", "UNKNOWN")
        
        print(f"\n{'='*60}")
        print(f"🔄 Processing Extended Application: {case_id}")
        print(f"{'='*60}\n")

        # ====================================
        # PIPELINE A: ML MODEL
        # ====================================
        print("📊 Running ML Pipeline...")
        ml_result = self.ml_agent.predict(application_data)
        print(f"   ✓ ML Risk Score: {ml_result['ml_risk_score']}")
        print(f"   ✓ ML Risk Level: {ml_result['ml_risk_level']}")
        print(f"   ✓ ML Prediction: {ml_result['ml_prediction']}\n")

        # ====================================
        # PIPELINE B: QDRANT/RAG
        # ====================================
        print("🔍 Running Qdrant/RAG Pipeline...")
        
        # Convert structured data to text summary for embedding
        text_summary = self._generate_text_summary(application_data)
        print(f"   ✓ Generated text summary ({len(text_summary)} chars)")

        # Create embedding
        embedding = self.embedding_agent.embed(text_summary)
        print(f"   ✓ Generated embedding (dim={len(embedding)})")

        # Retrieve similar cases
        retrieval_result = self.retrieval_agent.retrieve(
            query_vector=embedding,
            top_k=5
        )
        top_similarity = retrieval_result.get("top_similarity", 0.0)
        print(f"   ✓ Retrieved similar cases (top similarity: {top_similarity:.3f})")

        # Build simplified client profile for traditional pipeline
        client_profile = self._extract_client_profile(application_data)

        # Fraud detection
        fraud_result = self.fraud_agent.evaluate(
            client_profile=client_profile,
            retrieval_result=retrieval_result
        )
        print(f"   ✓ Fraud risk: {fraud_result['fraud_risk_level']}")

        # Risk evaluation (traditional)
        llm_summary = {
            "top_similarity": top_similarity,
            "similar_cases": retrieval_result.get("similar_cases", [])
        }
        risk_result = self.risk_agent.evaluate(
            client_profile=client_profile,
            llm_summary=llm_summary
        )
        print(f"   ✓ Traditional risk: {risk_result['risk_level']}")

        # Scenario generation
        scenario_result = self.scenario_agent.generate_scenarios(
            fraud_result=fraud_result,
            risk_result=risk_result,
            llm_summary=llm_summary
        )
        print(f"   ✓ Best scenario: {scenario_result['best_scenario']}\n")

        # ====================================
        # COMBINE RESULTS
        # ====================================
        print("🎯 Combining ML and Qdrant results...")
        
        # Decision from traditional pipeline
        qdrant_decision = self.decision_agent.run(
            top_similarity=top_similarity,
            fraud_result=fraud_result,
            scenario_result=scenario_result,
            risk_result=risk_result
        )

        # Combine both assessments
        final_result = self._combine_decisions(
            ml_result=ml_result,
            qdrant_decision=qdrant_decision,
            fraud_result=fraud_result,
            risk_result=risk_result,
            scenario_result=scenario_result,
            top_similarity=top_similarity
        )

        print(f"   ✓ Final decision: {final_result['final_decision']}")
        print(f"   ✓ Confidence: {final_result['confidence']}")
        print(f"\n{'='*60}\n")

        return final_result

    def _generate_text_summary(self, application: Dict[str, Any]) -> str:
        """
        Convert structured application data to text summary for embedding.
        This allows the Qdrant pipeline to work with the new data format.
        """
        client = application.get("client_identity", {})
        personal = application.get("personal_situation", {})
        professional = application.get("professional_situation", {})
        financial = application.get("financial_situation", {})
        credit = application.get("credit_request", {})
        behavioral = application.get("behavioral_indicators", {})
        risks = application.get("risk_checklist", {})

        summary_parts = []

        # Client info
        summary_parts.append(
            f"Client âgé de {client.get('age')} ans, "
            f"statut {client.get('client_status')}, "
            f"ancienneté bancaire {client.get('banking_seniority_years', 0)} ans."
        )

        # Professional
        summary_parts.append(
            f"Situation professionnelle: {professional.get('professional_status')}, "
            f"secteur {professional.get('sector', 'non spécifié')}, "
            f"ancienneté {professional.get('seniority_years', 0)} ans, "
            f"stabilité {professional.get('stability')}."
        )

        # Financial
        summary_parts.append(
            f"Revenu mensuel net: {financial.get('monthly_income_net')} €, "
            f"charges fixes: {financial.get('monthly_fixed_expenses')} €, "
            f"taux d'endettement: {financial.get('debt_ratio', 0)*100:.1f}%, "
            f"historique bancaire: {financial.get('banking_history')}."
        )

        # Credit request
        summary_parts.append(
            f"Demande de crédit {credit.get('credit_type')} de {credit.get('amount_requested')} € "
            f"sur {credit.get('duration_months')} mois, "
            f"pour {credit.get('purpose')}."
        )

        # Behavioral
        summary_parts.append(
            f"Indicateurs comportementaux: stress niveau {behavioral.get('stress_level')}, "
            f"urgence {behavioral.get('urgency_level')}, "
            f"clarté du projet {behavioral.get('project_clarity')}, "
            f"cohérence {behavioral.get('discourse_coherence')}."
        )

        # Risk flags
        risk_flags = []
        if risks.get('professional_instability'): risk_flags.append("instabilité professionnelle")
        if risks.get('high_debt'): risk_flags.append("endettement élevé")
        if risks.get('spouse_income_dependency'): risk_flags.append("dépendance revenu conjoint")
        if risks.get('non_priority_project'): risk_flags.append("projet non prioritaire")
        if risks.get('excessive_urgency'): risk_flags.append("urgence excessive")
        if risks.get('incoherent_discourse'): risk_flags.append("discours incohérent")
        
        if risk_flags:
            summary_parts.append(f"Risques identifiés: {', '.join(risk_flags)}.")

        return " ".join(summary_parts)

    def _extract_client_profile(self, application: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract client profile in format expected by traditional agents.
        Maps new schema fields to legacy field names.
        """
        financial = application.get("financial_situation", {})
        professional = application.get("professional_situation", {})
        
        # Map stability enum to score
        stability_map = {"LOW": 0.3, "MEDIUM": 0.5, "HIGH": 0.8}
        stability_score = stability_map.get(professional.get("stability"), 0.5)

        return {
            "monthly_income": financial.get("monthly_income_net", 0),
            "monthly_expenses": financial.get("monthly_fixed_expenses", 0),
            "debt_ratio": financial.get("debt_ratio", 0) or 0,
            "stability_score": stability_score
        }

    def _combine_decisions(
        self,
        ml_result: Dict[str, Any],
        qdrant_decision: Dict[str, Any],
        fraud_result: Dict[str, Any],
        risk_result: Dict[str, Any],
        scenario_result: Dict[str, Any],
        top_similarity: float
    ) -> Dict[str, Any]:
        """
        Combine ML and Qdrant pipeline results into final decision.
        
        Strategy:
        - If either pipeline flags high fraud risk → REJECT
        - If both agree on ACCEPT → ACCEPT with high confidence
        - If they disagree → MANUAL_REVIEW required
        - Use weighted average of confidence scores
        """
        mode = qdrant_decision.get("mode", "NORMAL")
        
        # Handle special modes first
        if mode == "FRAUD_STOP":
            return {
                "final_decision": "REJECT",
                "reason": "FRAUD_DETECTED",
                "confidence": qdrant_decision.get("confidence", 0.9),
                "mode": "FRAUD_STOP",
                "ml_assessment": ml_result,
                "qdrant_assessment": qdrant_decision,
                "action": "SEND_TO_INVESTIGATION"
            }
        
        if mode == "COLD_START":
            # Rely more on ML model in cold start
            return {
                "final_decision": ml_result["ml_prediction"],
                "reason": "COLD_START_ML_DECISION",
                "confidence": round(1 - ml_result["ml_risk_score"], 2),
                "mode": "COLD_START",
                "ml_assessment": ml_result,
                "qdrant_assessment": qdrant_decision,
                "human_validation_required": True
            }

        # NORMAL mode - combine both assessments
        ml_accepts = ml_result["ml_prediction"] == "ACCEPT"
        qdrant_accepts = qdrant_decision.get("final_decision") == "ACCEPT"

        # Check agreement
        if ml_accepts and qdrant_accepts:
            # Both agree on ACCEPT
            avg_confidence = (
                (1 - ml_result["ml_risk_score"]) * 0.5 +
                qdrant_decision.get("confidence", 0.5) * 0.5
            )
            return {
                "final_decision": "ACCEPT",
                "reason": "BOTH_MODELS_AGREE_ACCEPT",
                "confidence": round(avg_confidence, 2),
                "mode": "NORMAL",
                "conditions": qdrant_decision.get("conditions", []),
                "ml_assessment": ml_result,
                "qdrant_assessment": qdrant_decision
            }
        
        elif not ml_accepts and not qdrant_accepts:
            # Both agree on REJECT
            avg_confidence = (
                ml_result["ml_risk_score"] * 0.5 +
                (1 - qdrant_decision.get("confidence", 0.5)) * 0.5
            )
            return {
                "final_decision": "REJECT",
                "reason": "BOTH_MODELS_AGREE_REJECT",
                "confidence": round(avg_confidence, 2),
                "mode": "NORMAL",
                "ml_assessment": ml_result,
                "qdrant_assessment": qdrant_decision
            }
        
        else:
            # Disagreement - require manual review
            # Use ML as tiebreaker but flag for review
            final_decision = ml_result["ml_prediction"]
            return {
                "final_decision": final_decision,
                "reason": "MODELS_DISAGREE",
                "confidence": 0.5,  # Low confidence due to disagreement
                "mode": "MANUAL_REVIEW_REQUIRED",
                "ml_assessment": ml_result,
                "qdrant_assessment": qdrant_decision,
                "human_validation_required": True,
                "conflict_details": {
                    "ml_says": ml_result["ml_prediction"],
                    "qdrant_says": qdrant_decision.get("final_decision"),
                    "ml_confidence": round(1 - ml_result["ml_risk_score"], 2),
                    "qdrant_confidence": qdrant_decision.get("confidence", 0)
                }
            }
