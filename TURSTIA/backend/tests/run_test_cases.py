import os
import json
from backend.agents.embedding_agent import EmbeddingAgent
from backend.agents.retrieval_agent import QdrantRetrievalAgent
from backend.agents.decision_agent import DecisionAgent
from backend.agents.learning_loop_agent import LearningLoopAgent

# =============================
# Mock results pour test DecisionAgent
# =============================
fraud_result = {
    "fraud_risk_level": "LOW",
    "fraud_similarity": 0.0,
    "anomaly_score": 0.0
}

scenario_result = {"best_scenario": "ACCEPT"}
risk_result = {"risk_level": "LOW", "default_probability": 0.05}

# =============================
# Instanciation des agents
# =============================
decision_agent = DecisionAgent()
embedding_agent = EmbeddingAgent()
retrieval_agent = QdrantRetrievalAgent()
learning_agent = LearningLoopAgent()

# =============================
# Répertoire des fichiers
# =============================
base_dir = os.path.dirname(__file__)

# =============================
# Liste des JSON à tester
# =============================
test_files = [
    "input_application_normal.json",
    "input_application_fraud.json",
    "input_application_cold.json"
]

for file in test_files:
    print(f"\n--- Testing {file} ---")
    file_path = os.path.join(base_dir, file)
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}, skipping.")
        continue

    with open(file_path) as f:
        app = json.load(f)
        print(f"Loaded {file}:", app)

    # -----------------------------
    # Embedding
    # -----------------------------
    embedding_result = embedding_agent.run(
        chunks=[{"text": str(app)}],
        final_profile=app,
        loan_request={"loan_amount": app.get("loan_amount", 10000),
                      "term_months": app.get("term_months", 36)}
    )

    # Si EmbeddingAgent ne retourne rien, on mock un vecteur
    if embedding_result is None:
        embedding_result = {}

    if "vector" not in embedding_result or embedding_result["vector"] is None:
        embedding_result["vector"] = [0.0] * 128  # vecteur factice de dimension 128
        
    # -----------------------------
    # Decision
    # -----------------------------

    # Dictionnaires de test spécifiques
    test_inputs = {
        "input_application_normal.json": {
            "top_similarity": 0.85,
            "fraud_result": {"fraud_risk_level": "LOW", "fraud_similarity": 0.0, "anomaly_score": 0.0},
            "scenario_result": {"best_scenario": "ACCEPT"},
            "risk_result": {"risk_level": "LOW", "default_probability": 0.05}
        },
        "input_application_fraud.json": {
            "top_similarity": 0.7,
            "fraud_result": {"fraud_risk_level": "HIGH", "fraud_similarity": 0.95, "anomaly_score": 0.9},
            "scenario_result": {"best_scenario": "REJECT"},
            "risk_result": {"risk_level": "HIGH", "default_probability": 0.5}
        },
        "input_application_cold.json": {
            "top_similarity": 0.2,
            "fraud_result": {"fraud_risk_level": "LOW", "fraud_similarity": 0.0, "anomaly_score": 0.0},
            "scenario_result": {"best_scenario": "ACCEPT_WITH_GUARANTEE"},
            "risk_result": {"risk_level": "MEDIUM", "default_probability": 0.1}
        }
    }
    inputs = test_inputs[file]

    decision_result = decision_agent.run(
        top_similarity=inputs["top_similarity"],
        fraud_result=inputs["fraud_result"],
        scenario_result=inputs["scenario_result"],
        risk_result=inputs["risk_result"]
    )

    print("Decision output:", json.dumps(decision_result, indent=2))
