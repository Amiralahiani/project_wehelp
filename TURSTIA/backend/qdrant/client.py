from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from backend.config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION

_qdrant_client = None


def get_qdrant_client():
    """
    Retourne une instance unique du client Qdrant (Cloud)
    """
    global _qdrant_client

    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )

    return _qdrant_client

def check_collection_exists():
    client = get_qdrant_client()
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if QDRANT_COLLECTION not in names:
        raise RuntimeError(
            f"Qdrant collection '{QDRANT_COLLECTION}' not found"
        )

def check_collection_config(expected_dim: int = 384):
    """
    Vérifie que la collection a la bonne dimension
    et utilise la cosine similarity
    """
    client = get_qdrant_client()
    info = client.get_collection(QDRANT_COLLECTION)

    # Cas simple (1 seul vecteur)
    vectors_config = info.config.params.vectors

    if hasattr(vectors_config, "size"):
        size = vectors_config.size
        distance = vectors_config.distance
    else:
        # sécurité si multi-vector (pas notre cas)
        raise RuntimeError("Unexpected vector configuration")

    if size != expected_dim:
        raise RuntimeError(
            f"Vector size mismatch: expected {expected_dim}, got {size}"
        )

    if distance != Distance.COSINE:
        raise RuntimeError(
            f"Distance mismatch: expected COSINE, got {distance}"
        )

    return True