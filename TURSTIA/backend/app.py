
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pprint
from fastapi import Body
from fastapi import APIRouter
from backend.agents.supervisor_agent import SupervisorAgent
import traceback
from backend.agents.document_agent import run_document_agent
from backend.agents.document_agent import run_document_agent
from backend.agents.profile_fusion_agent import build_final_profile

from backend.agents.learning_loop_agent import LearningLoopAgent
from backend.schemas.expanded_application import ExpandedApplicationPackage
from backend.services.extended_submission_service import ExtendedSubmissionService

import json
from pathlib import Path
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends
from backend.database.security import get_current_user
from backend.database.auth import router as auth_router

# Initialisation de l'app FastAPI
app = FastAPI()

# Inclusion des routes d'authentification
app.include_router(auth_router, prefix="/auth")

# Configuration du CORS pour autoriser les requêtes depuis le frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model pour la requete de l'outcome
class OutcomeRequest(BaseModel):
    case_id: str
    outcome: str  
    loss_amount: float = 0.0

# Initialisation de l'agent de l'apprentissage
learning_agent = LearningLoopAgent()

# Initialisation du service de soumission étendue
extended_submission_service = ExtendedSubmissionService()

# Endpoint pour soumettre l'oucome réel d'un dossier
@app.post("/outcome")
def submit_outcome(request: OutcomeRequest):
    """
    Endpoint appelé quand l'outcome réel du dossier est connu.
    """

    try:
        result = learning_agent.run(
            case_id=request.case_id,
            outcome=request.outcome,
            loss_amount=request.loss_amount
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print(f"Error in submit_outcome: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Définition du fichier d’audit
AUDIT_LOG_FILE = Path("backend/logs/audit_log.jsonl")

# Endpoint pour récupérer les logs d'audit
@app.get("/audit")
def get_audit_logs(case_id: str = Query(None), user=Depends(get_current_user)):
    """
    Retourne les événements d'audit.
    Optionnellement filtrés par case_id.
    """

    if not AUDIT_LOG_FILE.exists():
        return []

    events = []

    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)

            if case_id:
                if event.get("case_id") == case_id:
                    events.append(event)
            else:
                events.append(event)

    return events




@app.post("/api/document-agent/test")
def test_document_agent(payload: dict = Body(...)):
    try:
        print("\n🔥 /api/document-agent/test CALLED 🔥\n")
        pprint.pprint(payload)

        case_id = payload.get("case_id")
        documents = payload.get("documents", [])
        applicant_form = payload.get("applicant_form", {})

        result = run_document_agent(
            case_id=case_id,
            documents=documents
        )

        return {
            "case_id": case_id,
            "document_analysis": result
        }

    except Exception as e:
        print("❌ DOCUMENT AGENT ERROR")
        traceback.print_exc()

        return {
            "error": "DOCUMENT_AGENT_FAILED",
            "message": str(e)
        }

@app.post("/api/complete-evaluation")
def complete_evaluation(payload: dict = Body(...)):

    case_id = payload.get("case_id")
    applicant_form = payload.get("applicant_form", {})
    loan_request = payload.get("loan_request", {})
    documents = payload.get("documents", [])

    # AGENT 1
    doc_analysis = run_document_agent(
        case_id=case_id,
        documents=documents
    )

    # AGENT 2
    fusion_result = build_final_profile(
        case_id=case_id,
        applicant_form=applicant_form,
        loan_request=loan_request,
        doc_signals=doc_analysis.doc_signals
    )

    return {
        "case_id": case_id,
        "document_analysis": doc_analysis,
        "profile_fusion": fusion_result
    }


router = APIRouter()
supervisoragent = SupervisorAgent()

@router.post("/submit-application")
def submit_application(payload: dict):
    return supervisoragent.run(payload)



@app.post("/api/submit-application")
def submit_application(payload: dict):
    supervisor = SupervisorAgent()
    return supervisor.run(payload)


@app.post("/api/submit-extended")
def submit_extended_application(application: ExpandedApplicationPackage):
    """
    Endpoint pour soumettre le formulaire étendu de débriefing.
    Traite l'application via les deux pipelines (ML + Qdrant) et combine les résultats.
    """
    try:
        print(f"\n{'='*60}")
        print("📋 Extended Application Submission Received")
        print(f"{'='*60}\n")
        
        # Convert Pydantic model to dict for processing
        application_dict = application.dict()
        
        # Process through dual pipeline
        result = extended_submission_service.process_application(application_dict)
        
        return {
            "success": True,
            "case_id": application.case_id,
            "evaluation_result": result
        }
        
    except Exception as e:
        print(f"❌ Error in submit_extended_application: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing extended application: {str(e)}"
        )


