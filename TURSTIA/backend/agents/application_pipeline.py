from backend.agents.document_agent import run_document_agent
from backend.agents.profile_fusion_agent import build_final_profile

def run_full_pipeline(case_id, applicant_form, loan_request, documents):

    # AGENT 1 — extraction
    doc_result = run_document_agent(
        case_id=case_id,
        documents=documents
    )

    # AGENT 2 — fusion
    fusion_result = build_final_profile(
        case_id=case_id,
        applicant_form=applicant_form,
        loan_request=loan_request,
        doc_signals=doc_result.doc_signals
    )

    return {
        "doc_analysis": doc_result,
        "profile_analysis": fusion_result
    }
