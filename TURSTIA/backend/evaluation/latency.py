# Full latency evaluation for TRUSTIA agents


import time
import random
from statistics import mean

from backend.agents.embedding_agent import EmbeddingAgent
from backend.agents.retrieval_agent import QdrantRetrievalAgent
from backend.agents.decision_agent import DecisionAgent
from backend.agents.learning_loop_agent import LearningLoopAgent

from backend.qdrant.client import get_qdrant_client
from backend.config import QDRANT_COLLECTION


# ===============================
# Evaluation config
# ===============================

N_RUNS = 20
POOL_LIMIT = 100
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# ===============================
# Utils
# ===============================

def measure(fn):
    """Simple wall-clock timer (ms)."""
    t0 = time.perf_counter()
    out = fn()
    return out, (time.perf_counter() - t0) * 1000


# ===============================
# Main
# ===============================

def main():

    # Instantiate agents
    embedding_agent = EmbeddingAgent()
    retrieval_agent = QdrantRetrievalAgent()
    decision_agent = DecisionAgent()
    learning_agent = LearningLoopAgent()

    # -------------------------------
    # Prepare test data
    # -------------------------------

    dummy_chunks = [
        {"text": "Applicant is freelance with monthly income of 900 TND."},
        {"text": "Loan request of 10,000 TND over 36 months for business equipment."}
    ]

    dummy_profile = {
        "employment_type": "Freelance",
        "sector": "IT",
        "monthly_income": 900,
        "monthly_expenses": 650,
        "debt_ratio": 0.72,
        "stability_score": 0.55,
        "late_payments": 1,
        "other_loans_count": 1
    }

    dummy_loan = {
        "loan_amount": 10000,
        "term_months": 36,
        "product": "Personal Loan"
    }

    # Load existing cases for retrieval / learning loop
    client = get_qdrant_client()
    points, _ = client.scroll(
        collection_name=QDRANT_COLLECTION,
        limit=POOL_LIMIT,
        with_payload=True,
        with_vectors=True
    )

    test_points = [
        p for p in points
        if p.payload and p.payload.get("case_id") and p.vector
    ]

    if not test_points:
        raise RuntimeError("No points found in Qdrant for latency evaluation")

    # -------------------------------
    # 1️⃣ Embedding Agent latency
    # -------------------------------

    embed_times = []

    for _ in range(N_RUNS):
        _, dt = measure(lambda: embedding_agent.run(
            chunks=dummy_chunks,
            final_profile=dummy_profile,
            loan_request=dummy_loan
        ))
        embed_times.append(dt)

    # -------------------------------
    # 2️⃣ Retrieval Agent latency
    # -------------------------------

    retrieval_times = []

    for _ in range(N_RUNS):
        p = random.choice(test_points)
        _, dt = measure(lambda: retrieval_agent.run(
            case_id=p.payload["case_id"],
            case_vector=p.vector,
            feature_payload={}
        ))
        retrieval_times.append(dt)

    # -------------------------------
    # 3️⃣ Decision Agent latency
    # -------------------------------

      # -------------------------------
        # Dummy upstream agent outputs
        # -------------------------------

        dummy_top_similarity = 0.82

        dummy_fraud_result = {
            "fraud_score": 0.12,
            "fraud_risk_level": "LOW",
            "anomaly_score": 0.08,
            "fraud_similarity": 0.2,
            "fraud_flag": False
        }

        dummy_risk_result = {
            "risk_score": 0.45,
            "risk_level": "MEDIUM",
            "debt_pressure": 0.5,
            "instability_risk": 0.4,
            "risk_flag": False,
            "risk_level": "LOW",
            "default_probability": 0.08
        }

        dummy_scenario_result = {
            "best_scenario": "STANDARD_PLAN",
            "best_scenario": "ACCEPT",
            "recommended_installment": 320,
            "scenario_score": 0.7,
            "affordability_ratio": 0.35
        }

        decision_times = []

        for _ in range(N_RUNS):
            _, dt = measure(lambda: decision_agent.run(
                dummy_top_similarity,
                dummy_fraud_result,
                dummy_scenario_result,
                dummy_risk_result
            ))
            decision_times.append(dt)


    # -------------------------------
    # 4️⃣ Learning Loop Agent latency
    # (optional but measured)
    # -------------------------------

    learning_times = []

    sample_case_id = test_points[0].payload["case_id"]

    for _ in range(min(5, N_RUNS)):  # avoid too many DB writes
        _, dt = measure(lambda: learning_agent.run(
            case_id=sample_case_id,
            outcome="REPAID",
            loss_amount=0.0
        ))
        learning_times.append(dt)

    # -------------------------------
    # Results
    # -------------------------------

    print("\n===== LATENCY EVALUATION (ms) =====")
    print(f"Embedding Agent      : {mean(embed_times):.2f} ms")
    print(f"Retrieval Agent      : {mean(retrieval_times):.2f} ms")
    print(f"Decision Agent       : {mean(decision_times):.2f} ms")
    if learning_times:
        print(f"Learning Loop Agent  : {mean(learning_times):.2f} ms")
    print("==================================\n")


if __name__ == "__main__":
    main()
