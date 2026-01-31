from backend.qdrant.client import get_qdrant_client
from backend.config import QDRANT_COLLECTION
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = get_qdrant_client()

flt = Filter(
    must=[
        FieldCondition(
            key="case_id",
            match=MatchValue(value="NEW-1107")
        )
    ]
)

res = client.query_points(
    collection_name=QDRANT_COLLECTION,
    query=None,
    query_filter=flt,
    limit=1,
    with_payload=True,
    with_vectors=False
)

print(res.points[0].payload)
