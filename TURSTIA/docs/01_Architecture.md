# Technical Architecture

## High-Level Overview
The system is designed as a **multi-agent pipeline** orchestrated by a
Supervisor Agent.

Frontend → API Gateway → Supervisor Agent → Specialized Agents → Qdrant

## Global Pipeline
1. Application submission (form + documents)
2. Document Intelligence Agent
3. Profile Fusion & Validation Agent
4. Embedding / Representation Agent
5. Memory & Retrieval Agent (Qdrant)
6. Fraud & Anomaly Agent
7. Credit Risk Agent
8. Scenario Simulator Agent
9. Decision & Policy Agent
10. Explanation & Audit Agent
11. Learning Loop (post-decision)

## Architecture Principles
- Loose coupling between agents
- Clear input/output contracts
- Deterministic decision flow
- Explainability at each step

## Backend Components
- FastAPI: API Gateway
- Supervisor Agent: orchestration and routing
- Agents: independent logical modules
- Qdrant: vector memory storage
- Object storage: raw documents (references only)

## Frontend Components
- Dashboard with 3 main views:
  - Normal Case
  - Fraud Case
  - Cold Start
- API-driven UI (REST)
- Clear visualization of similarity, decision, and explanations
