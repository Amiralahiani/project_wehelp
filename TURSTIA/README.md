# TRUSTIA — Credit Decision & Explainability Platform ✅

**Résumé:** TRUSTIA est un prototype full‑stack pour l'évaluation de dossiers de crédit basé sur des embeddings textuels et Qdrant (vector DB). Le backend orchestre des agents métier (document parsing, embedding, retrieval, fraud, risk, scenario, explanation) et expose une API FastAPI ; le frontend Angular fournit une UI pour la soumission, la visualisation (Similarity Radar) et l'explication des décisions.


## Aperçu
- Langages: **Python (backend)**, **TypeScript/Angular (frontend)**
- DB vecteurs: **Qdrant**
- Embeddings: **sentence-transformers/all-MiniLM-L6-v2**
- UI: dashboard avec `SimilarityRadar` (visualisation des cas similaires)

---


## Architecture (vue d'ensemble)
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Angular SPA)                   │
│   - UI, Upload documents, Affichage résultats              │
│   - Services: api.service.ts pour communication             │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/REST
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend API (Python FastAPI/Flask)             │
│  - Orchestration (main.py, app.py)                         │
│  - Agents: document, embedding, retrieval, fraud, risk     │
│  - Services: parsing, règles métier                        │
│  - Logs audit (JSONL)                                       │
└────┬─────────────────────────────────────────────────┬──────┘
     │                                                  │
     ▼                                                  ▼
┌─────────────────────┐                    ┌──────────────────────┐
│   Qdrant (Vector DB)│                    │  Storage             │
│ - Embeddings        │                    │ - Documents (bruts)  │
│ - Métadonnées       │                    │ - Fichiers temp      │
│ - Recherche vect.   │                    │ - Logs audit         │
└─────────────────────┘                    └──────────────────────┘

## Fonctionnalités
- Ingestion et analyse de documents (extraction texte + signaux)
- Embeddings et indexation dans Qdrant
- Recherche vectorielle et agrégation des cas similaires
- Détection de fraude, scoring de risque, décision et explication
- Audit structuré (JSONL)
- Dashboard Angular avec visualisations (dont similarity radar)


## Pipeline
1) Soumission dossier + documents  
2) Analyse documents  
3) Fusion profil  
4) Embeddings  
5) Retrieval Qdrant  
6) Fraude  
7) Risque  
8) Scénarios  
9) Décision  
10) Explication + Audit  
11) Learning loop (post-décision)

## Flux principal de fonctionnement
1. Upload d'un document
Utilisateur envoie document via UI Angular.
API backend reçoit fichier → document_agent le traite.
document_parser extrait texte et métadonnées.

2. Indexation (embedding)
embedding_agent calcule embedding (vecteur).
Stockage dans Qdrant avec métadonnées.

3. Recherche & Décision
Utilisateur soumet requête de recherche.
retrieval_agent envoie requête vectorielle à Qdrant.
Résultats post-traités par decision_agent (règles métier, scoring).

4. Audit & Traçabilité
Chaque action critiques loggée dans backend/logs/audit_log.jsonl.
Format JSONL pour parsing et analytics.

5. Détection de fraude (optionnel)
fraud_agent analyse patterns suspects.
risk_agent scores le risque global.

## Arborescence (fichiers clés)
Project-root/
├── README.md                          # Ce fichier
├── backend/
│   ├── main.py                        # Point d'entrée / orchestration
│   ├── app.py                         # Configuration application & routes
│   ├── config.py                      # Paramètres d'environnement
│   ├── requirements.txt                # Dépendances Python
│   ├── agents/                         # Agents métier
│   │   ├── document_agent.py          # Ingestion / normalisation
│   │   ├── embedding_agent.py         # Conversion en vecteurs
│   │   ├── retrieval_agent.py         # Recherche vectorielle
│   │   ├── fraud_agent.py             # Détection fraude
│   │   ├── decision_agent.py          # Logique décision
│   │   ├── risk_agent.py              # Scoring risque
│   │   ├── audit_agent.py             # Audit & traçabilité
│   │   └── ...
│   ├── services/
│   │   ├── document_parser.py         # Extraction texte/métadonnées
│   │   └── fraud_service.py           # Orchestration fraude
│   ├── schemas/
│   │   ├── application_package.py     # DTO application
│   │   └── document_analysis.py       # DTO analyse document
│   ├── qdrant/
│   │   ├── client.py                  # Intégration Qdrant
│   │   ├── schema.py                  # Schéma vecteurs
│   │   └── Seed.py                    # Alimentation de la base
│   ├── api/
│   │   ├── evaluate.py                # Endpoint d'évaluation
│   │   └── submission.py              # Endpoint de soumission
│   ├── evaluation/
│   │   ├── latency.py                 # Mesure latence
│   │   ├── precision_k.py             # Calcul précision@K
│   │   └── umap_visualization.py      # Visualisation embeddings
│   ├── tests/                         # Suite de tests
│   │   ├── test_retrieval.py
│   │   ├── test_embedding.py
│   │   ├── test_pipeline.py
│   │   ├── test_decision_agent.py
│   │   └── ...
│   ├── logs/
│   │   └── audit_log.jsonl            # Logs d'audit
│   ├── storage/                       # Documents indexés
│   ├── tmp_docs/                      # Fichiers temporaires
│   └── utils/
│       ├── audit_logger.py            # Logging audit
│       ├── io.py                      # I/O utilitaires
│       └── timers.py                  # Mesure performances
├── frontend/
│   ├── package.json                   # Dépendances npm
│   ├── angular.json                   # Config Angular CLI
│   ├── tsconfig.json                  # Config TypeScript
│   ├── src/
│   │   ├── main.ts                    # Bootstrap app
│   │   ├── app/
│   │   │   ├── app.ts                 # Composant root
│   │   │   ├── app.routes.ts          # Routes principales
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts     # Communication backend
│   │   │   │   └── application.service.ts
│   │   │   ├── features/
│   │   │   │   └── submission/        # Feature soumission
│   │   │   ├── audit/                 # Vue audit
│   │   │   ├── outcome/               # Affichage résultats
│   │   │   └── similarity-radar/      # Visualisation
│   │   └── index.html                 # Template HTML
│   └── README.md
└── docs/
    ├── 00_Project_Vision.md           # Vision projet
    ├── 01_Architecture.md             # Architecture détaillée
    ├── 02_Data_Schema.md              # Schémas données
    └── 03_Demo_Script.md              # Script démo

## Configuration
Configurer `backend/config.py`  :
```bash
QDRANT_URL = "https://880b58fd-3475-43fb-b1d1-3d084b21b497.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.LHDHXiBzEP64sRK8XDGN81SFO_3F2CePlTTemz38KVM"
QDRANT_COLLECTION = "credit_cases"
```

## Seeding Qdrant (notebook)
Le notebook `backend/qdrant/Seed.ipynb` :
- génère un dataset synthétique, crée des textes descriptifs, calcule des embeddings et upsert vers Qdrant.

Procédure rapide:
1. Ouvrir le notebook ou exécuter les scripts Python en local
2. Définir `QDRANT_URL` et `QDRANT_API_KEY`
3. Exécuter les cellules pour créer collection et upsert points

---

## Lancement local

### 1) Démarrer le backend
```bash
uvicorn backend.app:app --reload --port 8000
```
API dispo sur `http://localhost:8000` (Swagger: `http://localhost:8000/docs`).

### 2) Démarrer le frontend
```bash
cd frontend
npm run start
# ou avec Angular CLI
ng serve -o
```
SPA dispo sur `http://localhost:4200`.

### 3) Vérifier les connexions
- Backend: `http://localhost:8000/docs`
- Frontend: `http://localhost:4200`

## Tests
```bash
# Tests unitaires
python -m backend.tests

# Exemple ciblé
pytest backend\tests\test_retrieval.py -v
```

### Tests disponibles (extraits)
Tests disponibles			---> Fichier Objectif
test_retrieval.py			---> Recherche vectorielle Qdrant (retrieval & radar)
test_embedding.py			---> Génération embeddings (EmbeddingAgent)
test_pipeline.py			---> End-to-end pipeline (risk → scenario → decision)
test_decision_agent.py		---> Logique décision (normal / cold / fraud cases)
test_risk_agent.py			---> Scoring risque (RiskAgent)
test_qdrant_client.py		---> Vérifie client Qdrant & config collection (dim=384)
test_profile_fusion.py		---> Fusion de profil (build_final_profile)
test_ocr.py				---> OCR (pytesseract extraction)
test_learning_loop_agent.py	---> Learning loop (mise à jour d'outcomes dans Qdrant)
test_supervisor.py		---> Supervisor scenarios (cold / fraud / normal)
test_scenario_agent.py		---> Simulation de scénarios décisionnels
test_persona4_agents.py		---> Tests intégrés : fraude, décision, explication, audit
test_per3.py			---> Exemple pipeline (risk → scenario → decision)
test_cases.py			---> Scénarios multiples pour tests décisionnels
run_test_cases.py		---> Script d'exécution pour JSON d'exemple (end-to-end)
testdecisonAgent.py		---> (placeholder / fichier vide)
FindPoint.py			---> Utilitaire : rechercher un point par case_id dans Qdrant

## Évaluation & Benchmarking

Latency
```bash
python -m  backend.evaluation.latency.py
```
Mesure les temps de réponse API.

Precision@K
```bash
python backend.evaluation.precision_k.py
```
Calcule accuracy de la recherche vectorielle.

Visualisation
```bash
python backend.evaluation.umap_visualization.py
```
Génère graph 2D des embeddings (UMAP).

## Logs et audits des modifications des dossiers
Format structuré (JSONL) dans les logs.


```bash
python -m backend.evaluation.latency
python backend.evaluation.precision_k
python backend.evaluation.umap_visualization
```
## Documentation
- `docs/00_Project_Vision.md`
- `docs/01_Architecture.md`
- `docs/02_Data_Schema.md`
- `docs/03_Demo_Script.md`

