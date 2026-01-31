#PDF → texte brut
import pdfplumber 
from typing import List, Dict

def parse_pdf(uri: str) -> List[Dict]:
    pages_content = []

    file_path = uri.replace("file://", "")

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages_content.append({
                "page": i + 1,
                "text": text.splitlines()
            })

    return pages_content
