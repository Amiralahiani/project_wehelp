from datetime import datetime

class AuditAgent:
    def log(self, case_id: str, decision: dict):
        return {
            "case_id": case_id,
            "timestamp": datetime.utcnow().isoformat(),
            "mode": decision["mode"],
            "decision": decision["decision"],
            "confidence": decision["confidence"]
        }
