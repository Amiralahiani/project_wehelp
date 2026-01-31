# evaluation de precision@k 

# evaluation/precision_k.py

import random
from statistics import mean

from backend.agents.retrieval_agent import QdrantRetrievalAgent
from backend.config import PRECISION_K

# ===============================
# Evaluation config
# ===============================

N_QUERIES = 30
RANDOM_SEED = 42
random.seed(RANDOM_SEED)


def is_relevant(query_payload, candidate_payload):
    """
    Ground truth:
    Relevant if same fraud_label AND same decision
    """
    return (
        query_payload.get("fraud_label") == candidate_payload.get("fraud_label")
        and query_payload.get("decision") == candidate_payload.get("decision")
    )


def main():
    agent = QdrantRetrievalAgent()

    # Load evaluation pool

    from backend.qdrant.client import get_qdrant_client
    from backend.config import QDRANT_COLLECTION

    client = get_qdrant_client()
    points, _ = client.scroll(
        collection_name=QDRANT_COLLECTION,
        limit=500,
        with_payload=True,
        with_vectors=True
    )

    # keep only labeled points
    pool = [
        p for p in points
        if p.payload
        and p.payload.get("decision") is not None
        and p.payload.get("fraud_label") is not None
    ]

    queries = random.sample(pool, min(N_QUERIES, len(pool)))

    precisions = []

    # Evaluate each query
    for q in queries:
        result = agent.run(
            case_id=q.payload["case_id"],
            case_vector=q.vector,
            feature_payload={}  
        )

        # rebuild ranked neighbors
        neighbors = []

        for c in result["similar_normal_cases"]:
            neighbors.append({
                "payload": {
                    "fraud_label": False,
                    "decision": c.get("decision")
                }
            })

        for c in result["similar_fraud_cases"]:
            neighbors.append({
                "payload": {
                    "fraud_label": True,
                    "decision": "FRAUD"
                }
            })

        neighbors = neighbors[:PRECISION_K]

        # Precision@k
        relevant = 0
        for n in neighbors:
            if is_relevant(q.payload, n["payload"]):
                relevant += 1

        precisions.append(relevant / PRECISION_K)

    # Results
    print("\n===== RETRIEVAL AGENT EVALUATION =====")
    print(f"Precision@{PRECISION_K}: {mean(precisions):.3f}")
    print("====================================\n")


if __name__ == "__main__":
    main()
