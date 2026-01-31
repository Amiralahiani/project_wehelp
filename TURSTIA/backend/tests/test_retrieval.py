from backend.agents.embedding_agent import EmbeddingAgent
from backend.agents.retrieval_agent import QdrantRetrievalAgent
from backend.utils.radar_builder import build_radar_points


# ===============================
# Données mock
# ===============================

final_profile = {
    "employment_type": "Freelance",
    "sector": "Digital Services",
    "monthly_income": 910,
    "monthly_expenses": 645,
    "debt_ratio": 0.71,
    "stability_score": 0.55,
    "late_payments": 1,
    "other_loans_count": 1
}

loan_request = {
    "loan_amount": 10000,
    "term_months": 36,
    "product": "Personal Loan"
}


# ===============================
# Test
# ===============================

def test_retrieval_agent():
    embedding_agent = EmbeddingAgent()
    retrieval_agent = QdrantRetrievalAgent()

    # ===============================
    # Construction des chunks de test
    # ===============================

    # ====== CAS NORMAL ======
    chunks_normal = [
        {
            "chunk_id": "C1",
            "section": "SUMMARY",
            "text": (
                    "Self-employed applicant working in the IT sector. "
                    "Requested a personal loan of ten thousand dinars for three years. "
                    "No fraud indicators detected."
            )
        }
    ]

    embedding_result_normal = embedding_agent.run(
        chunks=chunks_normal,
        final_profile=final_profile,
        loan_request=loan_request
    )

    result_normal = retrieval_agent.run(
        case_id="TEST-NORMAL",
        case_vector=embedding_result_normal["case_vector"],
        feature_payload=embedding_result_normal["feature_payload"]
    )

    radar_points = build_radar_points("TEST-NORMAL", result_normal)

    print("\n=== CAS NORMAL ===")
    print("Top similarity:", result_normal["top_similarity"])
    print("Normal cases:", len(result_normal["similar_normal_cases"]))
    print("Fraud cases:", len(result_normal["similar_fraud_cases"]))
    print("Radar points:", radar_points)

    # ====== CAS FRAUDE ======
    chunks_fraud = [
        {
            "chunk_id": "C2",
            "section": "SUMMARY",
            "text": (
                        "Applicant profile: Unemployed, last employment sector Retail. "
                        "Loan request of 25000 TND over 48 months. "
                        "Estimated default probability 25 percent. "
                        "Fraud detected: yes."
            )
        }
    ]

    embedding_result_fraud = embedding_agent.run(
        chunks=chunks_fraud,
        final_profile=final_profile,
        loan_request=loan_request
    )

    result_fraud = retrieval_agent.run(
        case_id="TEST-FRAUD",
        case_vector=embedding_result_fraud["case_vector"],
        feature_payload=embedding_result_fraud["feature_payload"]
    )

    print("\n=== CAS FRAUDE ===")
    print("Top similarity:", result_fraud["top_similarity"])
    print("Normal cases:", len(result_fraud["similar_normal_cases"]))
    print("Fraud cases:", len(result_fraud["similar_fraud_cases"]))

    print("\n✅ Deux scénarios testés (normal + fraude)")

    
if __name__ == "__main__":
    test_retrieval_agent()
