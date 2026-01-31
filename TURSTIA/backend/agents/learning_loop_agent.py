# ======================================
# Learning Loop Agent (Outcome Update)
# ======================================

from typing import Dict, Any

from qdrant_client.models import Filter, FieldCondition, MatchValue, Payload

from backend.qdrant.client import get_qdrant_client
from backend.config import QDRANT_COLLECTION
from backend.utils.timers import measure_latency
from backend.utils.audit_logger import log_audit_event


class LearningLoopAgent:

    @measure_latency("Learning Loop Agent")
    def run(self, case_id: str, outcome: str, loss_amount: float = 0.0) -> Dict[str, Any]:
        """
        Met à jour le payload d'un dossier existant dans Qdrant
        après avoir reçu l'outcome réel (REPAID / DEFAULT).
        """

        outcome = outcome.upper().strip()

        if outcome not in {"REPAID", "DEFAULT"}:
            raise ValueError("outcome must be 'REPAID' or 'DEFAULT'")

        client = get_qdrant_client()

        # 1) Retrouver le point via case_id (car l'ID Qdrant interne peut être différent)
        flt = Filter(
            must=[
                FieldCondition(
                    key="case_id",
                    match=MatchValue(value=case_id)
                )
            ]
        )

        found = client.query_points(
            collection_name=QDRANT_COLLECTION,
            query=None,              
            query_filter=flt,
            limit=1,
            with_payload=True,
            with_vectors=False
        ).points

        if not found:
            return {
                "status": "NOT_FOUND",
                "case_id": case_id,
                "message": "No matching case_id in Qdrant"
            }

        point_id = found[0].id

        # 2) Construire payload update
        payload_update: Payload = {
            "outcome": outcome,
            "default": True if outcome == "DEFAULT" else False,
            "loss_amount": float(loss_amount) if outcome == "DEFAULT" else 0.0
        }

        # 3) Mettre à jour le payload du point
        client.set_payload(
            collection_name=QDRANT_COLLECTION,
            payload=payload_update,
            points=[point_id],
            wait=True
        )

        # 4) log audit event
        log_audit_event({
            "agent": "LearningLoopAgent",
            "action": "UPDATE_OUTCOME",
            "case_id": case_id,
            "point_id": point_id,
            "payload_update": payload_update
        })


        return {
            "status": "UPDATED",
            "case_id": case_id,
            "point_id": point_id,
            "payload_update": payload_update
        }
