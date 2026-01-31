# ======================================
# Qdrant Retrieval Agent (search + stats)
# ======================================

from collections import defaultdict
from typing import List, Dict
from qdrant_client.models import PointStruct
import uuid
from qdrant_client.models import Filter, FieldCondition, MatchValue

from backend.qdrant.client import (
    get_qdrant_client,
    check_collection_exists,
    check_collection_config
)
from backend.config import QDRANT_COLLECTION, TOP_K_SIMILAR
from backend.utils.timers import measure_latency


class QdrantRetrievalAgent:

    @measure_latency("Qdrant Retrieval Agent")
    def run(self, case_id: str, case_vector: List[float], feature_payload: Dict):

        # Sécurité : vérifier collection
        check_collection_exists()
        check_collection_config(expected_dim=len(case_vector))

        client = get_qdrant_client()

        # ===============================
        # Recherche globale (top-k)
        # ===============================
        response = client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=case_vector,
            limit=TOP_K_SIMILAR,
            with_payload=True,
            with_vectors=False
        )

        results = response.points

        if not results:
            return {
                "top_similarity": 0.0,
                "similar_normal_cases": [],
                "similar_fraud_cases": [],
                "stats_by_decision": {}
            }

        top_similarity = results[0].score

        # ===============================
        # Séparer normal / fraude
        # ===============================
        similar_normal_cases = []
        similar_fraud_cases = []

        for r in results:
            payload = r.payload or {}

            if payload.get("fraud_label") is True:
                similar_fraud_cases.append({
                    "point_id": r.id,  
                    "case_id": payload.get("case_id"),
                    "score": r.score,
                    "fraud_type": payload.get("fraud_type", "unknown")
                })
            else:
                similar_normal_cases.append({
                    "point_id": r.id,    
                    "case_id": payload.get("case_id"),
                    "score": r.score,
                    "decision": payload.get("decision"),
                    "default": payload.get("default")
                })

        # ===============================
        # Stats par décision (NORMAL)
        # ===============================
        stats_by_decision = defaultdict(lambda: {
            "n": 0,
            "observed_default_rate": None
        })

        for c in similar_normal_cases:
            decision = c.get("decision")
            defaulted = c.get("default")

            if decision is None:
                continue

            stats_by_decision[decision]["n"] += 1

            if defaulted is not None:
                stats_by_decision[decision].setdefault("defaults", 0)
                stats_by_decision[decision]["defaults"] += int(defaulted)

        # Calcul taux observé
        for decision, stats in stats_by_decision.items():
            n = stats["n"]
            defaults = stats.get("defaults", 0)

            if n > 0:
                stats["observed_default_rate"] = round(defaults / n, 3)

            stats.pop("defaults", None)

        return {
            "top_similarity": round(top_similarity, 3),
            "similar_normal_cases": similar_normal_cases,
            "similar_fraud_cases": similar_fraud_cases,
            "stats_by_decision": dict(stats_by_decision)
        }
    
    def store_case(self, case_id: str, vector: list, payload: dict):
        client = get_qdrant_client()

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload=payload
        )

        client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=[point]
        )

        