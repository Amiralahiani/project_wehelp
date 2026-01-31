from fastapi import APIRouter
from schemas.application_package import ApplicationPackage
from backend.agents.document_agent import process_documents

router = APIRouter()

@router.post("/submit-application")
def submit_application(payload: ApplicationPackage):
    result = run_full_pipeline(
        case_id=payload.case_id,
        applicant_form=payload.applicant_form.model_dump(),
        loan_request=payload.loan_request.model_dump(),
        documents=[doc.dict() for doc in payload.documents]
    )

    return {
        "case_id": payload.case_id,
        "document_agent": result["doc_analysis"],
        "profile_agent": result["profile_analysis"]
    }
