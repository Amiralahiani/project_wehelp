#Schéma de sortie
from pydantic import BaseModel
from typing import List, Dict, Any

class Evidence(BaseModel):
    doc_id: str
    page: int
    lines: List[str]


class TextChunk(BaseModel):
    section: str
    text: str


class DocumentAnalysisResult(BaseModel):
    doc_signals: Dict[str, Any]
    chunks: List[TextChunk]
    evidence_map: List[Evidence]
