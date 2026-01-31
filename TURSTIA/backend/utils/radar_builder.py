# Build radar visualization points from retrieval result.

def build_radar_points(case_id: str, retrieval_result: dict):

    radar_points = []

    #  Current case 
    radar_points.append({
        "type": "CURRENT",
        "case_id": case_id,
        "score": 1.0
    })

    # Normal similar cases
    for c in retrieval_result.get("similar_normal_cases", []):
        radar_points.append({
            "type": "NORMAL",
            "case_id": c.get("case_id"),
            "score": round(float(c.get("score", 0)), 3),
            "decision": c.get("decision")
        })

    #  Fraud similar cases
    for c in retrieval_result.get("similar_fraud_cases", []):
        radar_points.append({
            "type": "FRAUD",
            "case_id": c.get("case_id"),
            "score": round(float(c.get("score", 0)), 3),
            "fraud_type": c.get("fraud_type", "unknown")
        })

    return radar_points
