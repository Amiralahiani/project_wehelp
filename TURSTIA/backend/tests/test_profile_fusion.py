import json
import pprint
from ..agents.profile_fusion_agent import build_final_profile

# Charger un exemple JSON
with open("backend/tests/input_application_normal.json") as f:
    data = json.load(f)

result = build_final_profile(
    case_id=data["case_id"],
    applicant_form=data["applicant_form"],
    loan_request=data["loan_request"],
    doc_signals=data["doc_signals"]
)

pprint.pprint(result.model_dump())
