# Demo & Jury Script

## Introduction (30 seconds)
We present a credit decision system based on similarity search using Qdrant.
Instead of relying only on scores, we reuse historical memory.

## Demo Flow

### Case 1 — Normal
- Show application profile
- Show similar cases retrieved from Qdrant
- Show scenario table
- Final decision with explanation

### Case 2 — Fraud Detected
- High similarity with fraud cases
- Workflow stopped
- Evidence and fraud signals displayed

### Case 3 — Cold Start
- No similar cases above threshold
- AI recommendation with low confidence
- Human validation required

## Key Messages to the Jury
- Qdrant is the system’s memory
- Decisions are explainable
- Edge cases are handled safely
- The architecture supports learning over time

## Conclusion
This prototype demonstrates how vector databases can improve
decision-making systems by adding memory, context, and transparency.
