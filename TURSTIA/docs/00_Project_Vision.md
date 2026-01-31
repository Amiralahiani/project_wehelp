# Project Vision — Credit Decision Memory System

## Context
This project is developed as part of the Qdrant Hackathon.
It demonstrates how vector databases and similarity search can be used
to support credit decision-making in a transparent and explainable way.

## Problem Statement
Traditional credit scoring systems rely mainly on static scores and
black-box models. They struggle with:
- explainability,
- fraud detection,
- cold-start situations (new profiles).

## Our Objective
Build a prototype of a **multi-agent credit decision system**
that uses **historical memory stored in Qdrant** to:
- retrieve similar past cases,
- detect fraud patterns,
- support decisions with explanations.

## Core Use Cases
1. **NORMAL CASE**
   - Similar historical cases found
   - Decision based on similarity + scenarios
2. **FRAUD DETECTED**
   - High similarity with known fraud cases
   - Credit workflow is stopped
3. **COLD START**
   - No sufficiently similar cases
   - Human validation required

## What We Deliver
- Multi-agent backend (FastAPI + Python)
- Vector database (Qdrant)
- Modern dashboard (Angular / React)
- Explainable decisions and audit logs
- Evaluation metrics

## What We Explicitly Do NOT Build
- No production-grade system
- No heavy ML model training
- No authentication or user management

## Guiding Principle
Architecture clarity, explainability, and proper use of vector memory
are prioritized over complexity.
