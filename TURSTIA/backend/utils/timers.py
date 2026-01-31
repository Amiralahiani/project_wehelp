#Mesure de latence: 
"""                 génération d’embedding
                    requête Qdrant
                    pipeline complet"""

import time
from functools import wraps
from backend.config import ENABLE_LATENCY_LOGGING


def measure_latency(label: str):
    """
    Décorateur pour mesurer le temps d'exécution d'une fonction
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()

            if ENABLE_LATENCY_LOGGING:
                elapsed_ms = (end - start) * 1000
                print(f"[LATENCY] {label}: {elapsed_ms:.2f} ms")

            return result
        return wrapper
    return decorator
