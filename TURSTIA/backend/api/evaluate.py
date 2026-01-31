from fastapi import APIRouter
from backend.agents.document_agent import run_document_agent
from backend.schemas.application_package import ApplicationPackage

router = APIRouter()


@router.post("/evaluate/documents")
def evaluate_documents(payload: ApplicationPackage):
    result = run_document_agent(
        case_id=payload.case_id,
        documents=[doc.dict() for doc in payload.documents]
    )
    return result
