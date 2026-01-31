# ===============================
# Embedding Agent 
# ===============================

from sentence_transformers import SentenceTransformer
import numpy as np

from backend.config import TEXT_EMBEDDING_MODEL
from backend.utils.timers import measure_latency

# Chargement du modèle texte
text_model = SentenceTransformer(TEXT_EMBEDDING_MODEL)



def build_embedding_text(final_profile, loan_request):
    dp = loan_request.get("default_probability", 0.25)
    fraud_flag = loan_request.get("fraud_label", False)

    return (
        f"Applicant profile: {final_profile.get('employment_type')}, "
        f"last employment sector {final_profile.get('sector')}. "
        f"Loan request of {loan_request.get('loan_amount')} TND "
        f"over {loan_request.get('term_months')} months. "
        f"Estimated default probability {round(dp * 100, 1)} percent. "
        f"Fraud detected: {'yes' if fraud_flag else 'no'}."
    )



# ===============================
# Embedding TEXTE (SEUL vecteur Qdrant)
# ===============================

def embed_text(chunks):

    texts = [c["text"] for c in chunks if c.get("text")]

    # Fallback si aucun document texte
    if not texts:
        texts = ["Applicant profile without documents"]

    # Embedding par chunk puis moyenne
    embeddings = text_model.encode(texts)
    return embeddings.mean(axis=0)


# ===============================
# Embedding Agent
# ===============================

class EmbeddingAgent:

    @measure_latency("Embedding Agent")
    def run(self, chunks, final_profile, loan_request, documents=None):

       if not chunks:
        chunks = [{
            "text": build_embedding_text(final_profile, loan_request)
        }]

        text_vector = embed_text(chunks)


        case_vector = text_vector.tolist()
        feature_payload = {
            "employment_type": final_profile.get("employment_type"),
            "sector": final_profile.get("sector"),
            "monthly_income": final_profile.get("monthly_income"),
            "monthly_expenses": final_profile.get("monthly_expenses"),
            "debt_ratio": final_profile.get("debt_ratio"),
            "stability_score": final_profile.get("stability_score"),
            "late_payments": final_profile.get("late_payments"),
            "other_loans_count": final_profile.get("other_loans_count"),
            "loan_amount": loan_request.get("loan_amount"),
            "term_months": loan_request.get("term_months"),
            "product": loan_request.get("product")
        }

        return {
            "case_vector": case_vector,       
            "feature_payload": feature_payload 
        }
