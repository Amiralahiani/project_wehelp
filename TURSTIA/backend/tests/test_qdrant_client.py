from backend.qdrant.client import (
    get_qdrant_client,
    check_collection_exists,
    check_collection_config
)

def test_collection_config():
    client = get_qdrant_client()
    assert client is not None

    check_collection_exists()
    check_collection_config(expected_dim=384)

    print("✅ Qdrant collection config OK (384 / cosine)")


if __name__ == "__main__":
    test_collection_config()
