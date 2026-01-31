# ======================================
# Audit Logger
# ======================================

import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("backend/logs/audit_log.jsonl")


def log_audit_event(event: dict):
    """
    Ajoute un événement dans le fichier d'audit (JSON lines)
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    event["timestamp"] = datetime.utcnow().isoformat()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
