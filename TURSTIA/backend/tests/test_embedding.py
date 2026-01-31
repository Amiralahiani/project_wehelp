from backend.agents.embedding_agent import EmbeddingAgent

# -------------------------------
# Données de test (mockées)
# -------------------------------

chunks = [
    {
        "chunk_id": "C1",
        "section": "FINANCE",
        "text": "Monthly income is 920. Monthly expenses are 640. Freelance worker."
    },
    {
        "chunk_id": "C2",
        "section": "CONTRACT",
        "text": "Contract duration is 6 months. Short-term freelance contract."
    }
]

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

# -------------------------------
# Test
# -------------------------------

def test_embedding_agent():
    agent = EmbeddingAgent()

    result = agent.run(
        chunks=chunks,
        final_profile=final_profile,
        loan_request=loan_request
    )

    # Assertions simples
    assert "case_vector" in result
    assert "feature_payload" in result

    case_vector = result["case_vector"]

    print("Vector length:", len(case_vector))
    print("First 5 values:", case_vector[:5])

    assert isinstance(case_vector, list)
    assert len(case_vector) == 384  # CRITIQUE

    print("✅ EmbeddingAgent test passed")


if __name__ == "__main__":
    test_embedding_agent()
